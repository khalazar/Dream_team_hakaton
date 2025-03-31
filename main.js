document.addEventListener("DOMContentLoaded", () => {
  // Находим все элементы управления вкладками и сами вкладки
  const tabLinks = document.querySelectorAll("a[data-tab]");
  const tabContents = document.querySelectorAll(".tab-content");
  const sidebarNavLinks = document.querySelectorAll(".sidebar-nav a[data-tab]");
  const mobileNavLinks = document.querySelectorAll(
    ".mobile-bottom-nav a[data-tab]"
  );

  // Функция переключения вкладок
  function switchTab(tabId) {
    // 1. Скрыть все вкладки контента
    tabContents.forEach((content) => {
      content.classList.remove("active");
    });

    // 2. Показать нужную вкладку контента
    const activeContent = document.getElementById(`tab-${tabId}`);
    if (activeContent) {
      activeContent.classList.add("active");
    } else {
      console.warn(`Tab content not found for ID: tab-${tabId}`);
      // Запасной вариант: показать первую вкладку, если запрошенная не найдена
      if (tabContents.length > 0) {
        tabContents[0].classList.add("active");
        // Обновляем tabId, чтобы подсветить правильную кнопку меню
        const firstTabId = tabContents[0].id.replace("tab-", "");
        updateMenuActiveState(firstTabId);
        return; // Выходим, так как вкладка уже показана
      }
    }

    // 3. Обновить активное состояние кнопок меню
    updateMenuActiveState(tabId);
  }

  // Функция обновления активного состояния кнопок меню
  function updateMenuActiveState(activeTabId) {
    // Обновить активное состояние для бокового меню (Desktop)
    sidebarNavLinks.forEach((link) => {
      const isLinkActive = link.dataset.tab === activeTabId;
      link.classList.toggle("active", isLinkActive);
      link.classList.toggle("btn-active", isLinkActive);
    });

    // Обновить активное состояние для нижнего меню (Mobile)
    mobileNavLinks.forEach((link) => {
      const isLinkActive = link.dataset.tab === activeTabId;
      link.classList.toggle("active", isLinkActive);
      // Обновляем цвет текста и иконки при активации
      link.classList.toggle("text-primary", isLinkActive);
    });
  }

  // --- Инициализация и обработчики событий ---

  // Навесить обработчики кликов на все ссылки-переключатели
  tabLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault(); // Отменить стандартное поведение ссылки
      const tabId = link.dataset.tab;
      switchTab(tabId);

      // Плавная прокрутка вверх на мобильных при смене вкладки
      if (window.innerWidth < 768) {
        // Медиа-точка md Tailwind
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    });
  });

  // Обработчик для гамбургер-кнопки (заглушка)
  const hamburgerButton = document.querySelector(
    '.mobile-bottom-nav button[aria-label="Открыть меню"]'
  );
  if (hamburgerButton) {
    hamburgerButton.addEventListener("click", () => {
      alert("Нажата кнопка меню (требуется доп. реализация)");
      // Здесь можно добавить логику для открытия/закрытия бокового меню на мобильных,
      // например, добавляя/удаляя класс 'hidden' у <aside>
    });
  }

  // Установить начальную активную вкладку при загрузке страницы
  function initializeActiveTab() {
    // Пытаемся найти вкладку, помеченную как 'active' в HTML
    const initialActiveContent = document.querySelector(".tab-content.active");
    let initialTab = "calendar"; // По умолчанию - календарь/расписание

    if (initialActiveContent && initialActiveContent.id) {
      initialTab = initialActiveContent.id.replace("tab-", "");
    } else if (
      !document.getElementById("tab-calendar") &&
      tabLinks.length > 0
    ) {
      // Если в HTML нет активной И нет вкладки календаря, берем первую попавшуюся
      const firstLink = document.querySelector("a[data-tab]");
      if (firstLink) {
        initialTab = firstLink.dataset.tab;
      }
    }
    // Явно активируем нужную вкладку (приоритет у 'calendar')
    switchTab(initialTab);
  }

  initializeActiveTab(); // Вызываем функцию инициализации
}); // Конец 'DOMContentLoaded'
