function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Intl.DateTimeFormat('en-US', options).format(date);
}

function handleEvent(element, event, callback) {
    if (element && typeof callback === 'function') {
        element.addEventListener(event, callback);
    }
}

function scrollToElement(element) {
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function toggleClass(element, className) {
    if (element) {
        element.classList.toggle(className);
    }
}