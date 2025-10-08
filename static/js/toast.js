function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toastComponent) return;

    toastComponent.classList.remove('toast-success', 'toast-error', 'toast-normal');
    if (type === 'success') {
        toastComponent.classList.add('toast-success');
        if(toastIcon) toastIcon.innerHTML = '✅';
    } else if (type === 'error' || type === 'danger') { 
        toastComponent.classList.add('toast-error');
        if(toastIcon) toastIcon.innerHTML = '❌';
    } else {
        toastComponent.classList.add('toast-normal');
        if(toastIcon) toastIcon.innerHTML = 'ℹ️';
    }
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    toastComponent.style.opacity = '1';
    toastComponent.style.transform = 'translateX(0)'; 

    setTimeout(() => {
        toastComponent.style.opacity = '0';
        toastComponent.style.transform = 'translateX(100%)';
    }, duration);
}