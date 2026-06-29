function loadCategories(typeId, selectedCategoryId = null, selectedSubcategoryId = null) {
    const categorySelect = document.getElementById('id_category');
    categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
    if (!typeId) {
        return;
    }
    fetch(`/ajax/categories/?type_id=${typeId}`)
        .then((response) => response.json())
        .then((data) => {
            data.forEach((category) => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                if (selectedCategoryId && String(category.id) === String(selectedCategoryId)) {
                    option.selected = true;
                }
                categorySelect.appendChild(option);
            });
            if (selectedCategoryId) {
                loadSubcategories(selectedCategoryId, selectedSubcategoryId);
            }
        });
}

function loadSubcategories(categoryId, selectedSubcategoryId = null) {
    const subcategorySelect = document.getElementById('id_subcategory');
    subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
    if (!categoryId) {
        return;
    }
    fetch(`/ajax/subcategories/?category_id=${categoryId}`)
        .then((response) => response.json())
        .then((data) => {
            data.forEach((subcategory) => {
                const option = document.createElement('option');
                option.value = subcategory.id;
                option.textContent = subcategory.name;
                if (selectedSubcategoryId && String(subcategory.id) === String(selectedSubcategoryId)) {
                    option.selected = true;
                }
                subcategorySelect.appendChild(option);
            });
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!typeSelect || !categorySelect || !subcategorySelect) {
        return;
    }

    const selectedCategoryId = categorySelect.value;
    const selectedSubcategoryId = subcategorySelect.value;

    if (typeSelect.value) {
        loadCategories(typeSelect.value, selectedCategoryId, selectedSubcategoryId);
    }

    let initialCategoryLoad = true;

    typeSelect.addEventListener('change', function () {
        initialCategoryLoad = false;
        loadCategories(this.value);
        subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
    });

    categorySelect.addEventListener('change', function () {
        loadSubcategories(this.value, initialCategoryLoad ? selectedSubcategoryId : null);
        initialCategoryLoad = false;
    });
});
