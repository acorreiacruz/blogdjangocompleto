const forms = document.querySelectorAll(".form-delete");
const buttonShowMenu = document.querySelector('.button-show-menu');
const buttonCloseMenu = document.querySelector('.button-close-menu');
const menuContainer = document.querySelector('.menu-container');
const formLogout = document.querySelector('.logout-form');
const linksLogoutForm = document.querySelectorAll('.link-logout-form');
const navLinks = document.querySelectorAll('.menu-nav a');
const buttonShowMenuVisibleClass = 'button-show-menu-visible';
const menuHiddenClass = 'menu-hidden';

const escope = () => {
    for(const form of forms){
        form.addEventListener('submit', (e) =>{
            e.preventDefault();

            const confirmDeletion = confirm("Você tem certeza que quer excluir esta receita ?");

            if(confirmDeletion){
                form.submit();
            }
        });
    }
}

const closeMenu = () => {
    buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
    menuContainer.classList.add(menuHiddenClass);
}

const showMenu = () => {
    buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
    menuContainer.classList.remove(menuHiddenClass);
}

const deactivateLinks = () => {
    for(const link of navLinks){
        link.style.visibility = 'hidden';
    }
}

const activateLinks = () => {
    for(const link of navLinks){
        link.style.visibility = 'visible';
    }
}

const menu = () =>{
    document.addEventListener('click',(e) => {
        const el = e.target;
        if(el.classList.contains('fa-bars')){
            showMenu();
            activateLinks();
        }
        if(el.classList.contains('fa-circle-xmark')){
            closeMenu();
            deactivateLinks();
        }
    });
}

const logout = () => {
    for(const link of linksLogoutForm){
        link.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        });
    }
}


deactivateLinks();
escope();
menu();
logout();
