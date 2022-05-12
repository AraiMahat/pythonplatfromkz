console.log("hello")


const modalBtns = [...document.getElementsByClassName('modal-button')]

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    console.log(modalBtn)
}))