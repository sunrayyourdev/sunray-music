function deleteConfirm(number) {
    return confirm('Are you sure you want to delete Song ' + number + "?");
}

function deleteAllConfirm(count) {
    if ( count === 0 ) {
        return alert('Unable to delete. No songs in trash');
    }
    return confirm('Are you sure you want to delete all songs in library?');
}


function permanentDeleteConfirm(number) {
    return confirm('Are you sure you want to permanently delete Song ' + number + "?");
}

function permanentDeleteAllConfirm(count) {
    if ( count === 0 ) {
        return alert('Unable to delete. No songs in trash');
    }
    return confirm('Are you sure you want to permanently delete all songs in Recently Deleted?');
}

function changeNavLinkColour() {
    let currentPageTitle = 'nav' + document.getElementById('title').innerHTML.slice(15).replace(' ', '');
    navLink = document.getElementById(currentPageTitle);
    if ( navLink ) {
        navLink.style.color = 'grey';
    }
}

function setTheme(currentTheme) {
    document.body.setAttribute('class', currentTheme.toLowerCase());
}

//function hideNavBar() {
//    console.log('1');
//    console.log(document.getElementById('navbar').innerHTML);
//    document.getElementByClass('nav').setAttribute('class', 'nav hide');
//}