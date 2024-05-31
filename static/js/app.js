const searchBox = document.querySelector('#searchBox');
const listContainer = document.querySelector('#choiceList');
const itemList = listContainer.querySelectorAll('span');

itemList.forEach(item => {
            item.style.display = 'none';
});
searchBox.addEventListener('input', () => {
    if (searchBox.value === '') {
        itemList.forEach(item => {
            item.style.display = 'none';
        });
    }
    itemList.forEach(item => {
        if (item.textContent.toLowerCase().includes(searchBox.value.toLowerCase())) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
})