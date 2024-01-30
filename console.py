#!/usr/bin/python3
"""Art & Culture console."""

import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.artist import Artist
from models.artwork import Artwork
from models.categories import Category
from models.message import Message
from models.comment import Comment
import shlex
import re

classes = {
        "BaseModel": BaseModel, "Artist": Artist, "Artwork": Artwork,
        "Category": Category, "Message": Message, "Comment": Comment
    }


class ANC(cmd.Cmd):
    """Art and culture console """
    prompt = '(A&C) '

    # ---------------------------- Cmd commands ------------------------------
    def emptyline(self):
        """Take care of empty line."""
        pass

    def default(self, s):
        """Take care of unrecognized commands."""
        # line = shlex.split(s)
        match = re.search(r"([A-Z]\w*)\.(\w+)\(([^()]*)\)", s)
        if match:
            class_name = match.group(1)
            objects = models.storage.all()
            if class_name in list(classes.keys()):
                command = match.group(2)
                if command == "all":
                    self.do_all(class_name)
                elif command == "count":
                    result = 0
                    for key, model in objects.items():
                        if key.startswith(class_name):
                            result += 1
                    print(result)
                elif command in ["show", "destroy", "update"]:
                    args = " ".join(match.group(3).split(","))
                    text = f"{class_name} {args}"
                    if args[-1] == "}":
                        # "38f22813-2753-4d42-b37c-57a17f1e4f88", {
                        #                          'first_name': "John",
                        #                          "age": 89
                        #                       }
                        match2 = re.search(
                                r'("[^"]*"), ({[^{}]*})', match.group(3)
                            )
                        id = match2.group(1)
                        attrs = match2.group(2)
                        for key, value in eval(attrs).items():
                            self.do_update(f"{class_name} {id} {key} {value}")
                    else:
                        eval(f"self.do_{command}('{text}')")
            else:
                print("** class doesn't exist **")
        else:
            return cmd.Cmd.default(self, s)

    # --------------------------- Main commands ------------------------------
    def do_create(self, s):
        """Create a new instance of BaseModel."""
        line = shlex.split(s)
        n = len(line)
        if n:
            class_name = line[0]
            args = {
                item.split("=")[0]: item.split("=")[1] for item in line[1:]
            }
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                new_model = eval(class_name)(**args)
                models.storage.new(new_model)
                models.storage.save()
                print(new_model.id)
        else:
            print("** class name missing **")

    def do_show(self, s):
        """Print string representation of instance based on class name."""
        line = shlex.split(s)
        n = len(line)
        if n:
            class_name = line[0]
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                if n < 2:
                    print("** instance id missing **")
                else:
                    objects = models.storage.all()
                    id = line[1]
                    if f"{class_name}.{id}" not in objects:
                        print("** no instance found **")
                    else:
                        if n > 2:
                            cls_2 = line[2]
                            print(
                                getattr(
                                    objects[
                                        f"{class_name}.{id}"
                                    ],
                                    cls_2
                                )
                            )
                        else:
                            print(objects[f"{class_name}.{id}"])
        else:
            print("** class name missing **")

    def do_destroy(self, s):
        """Delete an instance based on the class name and id."""
        line = shlex.split(s)
        n = len(line)
        if n:
            class_name = line[0]
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                if n < 2:
                    print("** instance id missing **")
                else:
                    objects = models.storage.all()
                    id = line[1]
                    if f"{class_name}.{id}" not in objects:
                        print("** no instance found **")
                    else:
                        del objects[f"{class_name}.{id}"]
                        models.storage.save()
        else:
            print("** class name missing **")

    def do_all(self, s):
        """Print all string representation of all instances."""
        line = shlex.split(s)
        n = len(line)
        objects = models.storage.all()
        result = []
        if n:
            class_name = line[0]
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                for key, model in objects.items():
                    if key.startswith(class_name):
                        result.append(str(model))
        else:
            for key, model in objects.items():
                result.append(str(model))
        if result:
            print(result)

    def do_allids(self, s):
        """Print all string representation of all instances with their ids."""
        line = shlex.split(s)
        n = len(line)
        objects = models.storage.all()
        result = []
        if n:
            class_name = line[0]
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                k = 0
                for key, model in objects.items():
                    if key.startswith(class_name):
                        result.append(f"{model.id}")
                        wcol = []
                        for col in line[1:]:
                            try:
                                result[k] += f" {getattr(model, col)}"
                            except Exception:
                                wcol.append(col)
                        k += 1
                if wcol:
                    print(f"** column/s '{wcol}' is/are incorrect **")
        else:
            for key, model in objects.items():
                result.append(str(model))
        if result:
            print(result)

    def do_append(self, s):
        line = shlex.split(s)
        n = len(line)
        if n:
            first_class_name = line[0]
            second_class_name = line[2]
            first_cls_id = line[1]
            second_cls_id = line[3]

            model_1 = models.storage.get(first_class_name, first_cls_id)
            model_2 = models.storage.get(second_class_name, second_cls_id)

            getattr(model_1, model_2.__tablename__).append(model_2)
            # eval(f"model_1.{model_2.__tablename__}.append(model_2)")
            models.storage.save()

    def do_update(self, s):
        """Update an instance based on the class name and id."""
        line = shlex.split(s)
        n = len(line)
        if n:
            class_name = line[0]
            if class_name not in list(classes.keys()):
                print("** class doesn't exist **")
            else:
                if n < 2:
                    print("** instance id missing **")
                else:
                    objects = models.storage.all()
                    id = line[1]
                    if f"{class_name}.{id}" not in objects:
                        print("** no instance found **")
                    else:
                        if n < 3:
                            print("** attribute name missing **")
                        else:
                            attr = line[2]
                            if n < 4:
                                print("** value missing **")
                            else:
                                value = line[3]
                                dont_touch = ["id", "created_at", "updated_at"]
                                if attr not in dont_touch:
                                    model = objects[f"{class_name}.{id}"]
                                    if hasattr(model, attr):
                                        t = type(getattr(model, attr))
                                        try:
                                            setattr(model, attr, t(value))
                                        except Exception:
                                            setattr(model, attr, value)
                                    else:
                                        setattr(model, attr, value)
                                    model.save()
        else:
            print("** class name missing **")

    def do_quit(self, line):
        """End of input stream."""
        return True

    def do_EOF(self, line):
        """End of input stream."""
        print()
        return True

    # --------------------------- Help commands ------------------------------
    def help_quit(self):
        """Help quit."""
        help_txt = """Used to Exit the interactive console"""
        print(help_txt)

    def help_create(self):
        """Help on create command."""
        help_txt = """create <ModelName>
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id. Ex:
        (hbnb) create BaseModel
        """
        print(help_txt)

    def help_show(self):
        """Help on show command."""
        help_txt = """show <ModelName> <id>
        Prints the string representation of an instance
        based on the class name and id.
        Ex:
        (hbnb) show BaseModel 1234-1234-1234
        """
        print(help_txt)

    def help_all(self):
        """Help on all command."""
        help_txt = """all [<ModelName>]
        Prints all string representation of all instances
        based or not on the class name. Ex:
        (hbnb) all BaseModel
        or
        (hbnb) all
        """
        print(help_txt)

    def help_destroy(self):
        """Help on destroy command."""
        help_txt = """destroy <BaseModel> <id>
        Deletes an instance
        based on the class name and id (save the change).
        Ex:
        (hbnb) destroy BaseModel 1234-1234-1234
        """
        print(help_txt)

    def help_update(self):
        """Help on update command."""
        help_txt = """update <BaseModel> <id> <attr name> <attr value>
         Updates an instance
         based on the class name and id by adding or updating attribute
         (save the change). Ex:
         (hbnb) update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        print(help_txt)


if __name__ == '__main__':
    ANC().cmdloop()
