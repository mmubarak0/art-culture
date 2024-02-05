const switchBtn = document.getElementById('btnSwitch')

const light = 'bi bi-brightness-high-fill'
const dark = 'bi bi-moon-stars-fill'
const prefferedMode = localStorage.getItem('prefferedMode')

if (prefferedMode && prefferedMode === 'dark') {
  document.documentElement.setAttribute('data-bs-theme', 'dark')
  switchBtn.firstElementChild.setAttribute('class', light)
}
switchBtn.addEventListener('click', () => {
  if (switchBtn.firstElementChild.getAttribute('class') === dark) {
    document.documentElement.setAttribute('data-bs-theme', 'dark')
    localStorage.setItem('prefferedMode', 'dark')
    switchBtn.firstElementChild.setAttribute('class', light)
  } else {
    document.documentElement.setAttribute('data-bs-theme', 'light')
    localStorage.setItem('prefferedMode', 'light')
    switchBtn.firstElementChild.setAttribute('class', dark)
  }
})
