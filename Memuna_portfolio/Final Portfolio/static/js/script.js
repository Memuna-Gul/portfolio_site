document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const closeBtn = document.querySelector('.close-menu');
    const navList = document.querySelector('.nav-list');
    const menuIcon = document.getElementById('menu-icon');

    function toggleMenu() {
        navList.classList.toggle('active');
        menuIcon.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    }

    function closeMenu() {
        navList.classList.remove('active');
        menuIcon.classList.remove('active');
        document.body.classList.remove('no-scroll');
    }

    // Toggle menu when hamburger is clicked
    hamburger.addEventListener('click', toggleMenu);

    // Close menu when close button is clicked
    closeBtn.addEventListener('click', closeMenu);

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navList.contains(e.target) && 
            !hamburger.contains(e.target) && 
            navList.classList.contains('active')) {
            closeMenu();
        }
    });

    // Close menu when pressing ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navList.classList.contains('active')) {
            closeMenu();
        }
    });

    // Close menu when clicking nav links
    document.querySelectorAll('.nav-list li').forEach(link => {
        link.addEventListener('click', closeMenu);
    });
});

const navs = document.querySelectorAll('.nav-list li');
const box = document.querySelector('.box');
const sections = document.querySelectorAll('.section');

const resumeLists = document.querySelectorAll('.resume-list');
const resumeBoxs = document.querySelectorAll('.resume-box');

const portfolioLists = document.querySelectorAll('.portfolio-list');
const portfolioBoxs = document.querySelectorAll('.portfolio-box');

// Navigation and section transitions
navs.forEach((nav, idx) => {
    nav.addEventListener('click', () => {
        // Update active nav item
        document.querySelector('.nav-list li.active').classList.remove('active');
        nav.classList.add('active');

        // Get all sections
        const sections = document.querySelectorAll('.section');

        // Hide all sections first
        sections.forEach(section => {
            section.classList.remove('active');
        });

        // Map index to section names for verification
        const sectionMap = ['home', 'about', 'resume', 'portfolio', 'contact'];
        const targetSection = document.querySelector(`.section.${sectionMap[idx]}`);

        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
});

// Resume section tabs
resumeLists.forEach((list, idx) => {
    list.addEventListener('click', () => {
        document.querySelector('.resume-list.active').classList.remove('active');
        list.classList.add('active');

        document.querySelector('.resume-box.active').classList.remove('active');
        resumeBoxs[idx].classList.add('active');
    });
});

// Portfolio section tabs
portfolioLists.forEach((list, idx) => {
    list.addEventListener('click', () => {
        document.querySelector('.portfolio-list.active').classList.remove('active');
        list.classList.add('active');

        document.querySelector('.portfolio-box.active').classList.remove('active');
        portfolioBoxs[idx].classList.add('active');
    });
});

// Ensure contact section is properly initialized
window.addEventListener('load', () => {
    sections[4].classList.remove('active');
    if (!sections[0].classList.contains('active')) {
        sections[4].classList.add('action-contact');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const navs = document.querySelectorAll('.nav-list li');
    const sections = document.querySelectorAll('.section');

    // Function to hide all sections
    function hideAllSections() {
        sections.forEach(section => {
            section.classList.remove('active');
        });
    }

    // Function to remove active class from all nav items
    function removeActiveNavs() {
        navs.forEach(nav => {
            nav.classList.remove('active');
        });
    }

    // Add click event listeners to navigation items
    navs.forEach((nav, index) => {
        nav.addEventListener('click', () => {
            // Remove active class from all sections and nav items
            hideAllSections();
            removeActiveNavs();

            // Add active class to clicked nav item
            nav.classList.add('active');

            // Determine which section to show based on index
            let sectionToShow;
            switch(index) {
                case 0:
                    sectionToShow = document.querySelector('.section.home');
                    break;
                case 1:
                    sectionToShow = document.querySelector('.section.about');
                    break;
                case 2:
                    sectionToShow = document.querySelector('.section.resume');
                    break;
                case 3:
                    sectionToShow = document.querySelector('.section.portfolio');
                    break;
                case 4:
                    sectionToShow = document.querySelector('.section.contact');
                    break;
            }

            if (sectionToShow) {
                sectionToShow.classList.add('active');
            }
        });
    });

    // Resume tab handling
    const resumeNavBtns = document.querySelectorAll('.resume-nav-btn');
    const resumeTabs = document.querySelectorAll('.resume-tab');

    resumeNavBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and tabs
            resumeNavBtns.forEach(b => b.classList.remove('active'));
            resumeTabs.forEach(t => t.classList.remove('active'));

            // Add active class to clicked button and corresponding tab
            btn.classList.add('active');
            const tabId = `${btn.dataset.tab}-tab`;
            document.getElementById(tabId).classList.add('active');
        });
    });
});