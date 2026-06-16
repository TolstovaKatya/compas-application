<script setup>
import { NMenu, NIcon } from "naive-ui"; 
import { h, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";  
import { computed } from "vue";
const router = useRouter(); 

const username = ref('')
const isMenu = ref(true)
const lastScrollY = ref(0)

const isAutentificated = computed(() => !!localStorage.getItem('access_token'))

const isMobileMenuOpen = ref(false)
const isMobile = ref(false)

const checkScreen = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) isMobileMenuOpen.value = false 
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const handleScroll = () => {
  const currentScrollY = window.scrollY

  if (currentScrollY > lastScrollY.value) {
    isMenu.value = false
  }

  else if (currentScrollY < lastScrollY.value) {
    isMenu.value = true
  }

  if (currentScrollY < 50) {
    isMenu.value = true
  }

  lastScrollY.value = currentScrollY
}

const scrollToSection = (e, sectionId) => {
  e.preventDefault(); 
  closeMobileMenu()
  
  if (window.location.pathname !== '/') {
    router.push('/').then(() => {
      setTimeout(() => {
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    });
  } else {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

const COLOR_NORMAL = '#ffffff';
const COLOR_HOVER = '#00B1FF';

const menuOptions = computed(() => {
  if(isAutentificated.value) {
    return[
      {
        label: () => h(
          "a",
          {
            href: "/",
            style: {
              color: COLOR_NORMAL,
              textDecoration: 'none',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_HOVER;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_NORMAL;
            }
          },
          "НА ГЛАВНУЮ"
        ),
        key: "main-page",
      },
      {
        label: () => h(
          "a",
          {
            href: "/lessons",
            style: {
              color: COLOR_NORMAL,
              textDecoration: 'none',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_HOVER;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_NORMAL;
            }
          },
          "К СПИСКУ УРОКОВ"
        ),
        key: "main-page",
      },
      {
        label: () => h(
          "a",
          {
            href: "/profile",
            style: {
              color: COLOR_HOVER,
              textDecoration: 'underline',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_NORMAL;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_HOVER;
            }
          },
          `${ username.value }`
        ),
        key: "main-page",
      }
    ]
  } else {
    return[
              {  
          label: () => h(
          "a",
          {
            href: "/",
            style: {
              color: COLOR_NORMAL,
              textDecoration: 'none',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_HOVER;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_NORMAL;
            },

            onClick: (e) => scrollToSection(e, 'first-block')
          },
          "О КОМПАС 3D"
        ),
        key: "about-compas",
      },

        {
          label: () => h(
          "a",
          {
            href: "/",
            style: {
              color: COLOR_NORMAL,
              textDecoration: 'none',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_HOVER;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_NORMAL;
            },
            onClick: (e) => scrollToSection(e, 'second-block')
          },
          "ЧЕМУ НАУЧИМСЯ"
        ),
        key: "skils",
      },

        {
          label: () => h(
          "a",
          {
            href: "/",
            style: {
              color: COLOR_NORMAL,
              textDecoration: 'none',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_HOVER;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_NORMAL;
            },
            onClick: (e) => scrollToSection(e, 'third-block')
          },
          "О КУРСЕ"
        ),
        key: "about-course",
      },

      {
        label: () => h(
          "a",
          {
            href: "/login",
            style: {
              color: COLOR_HOVER,
              textDecoration: 'underline',
              display: 'block',
              width: '100%',
              height: '100%',
              transition: 'color 0.3s'
            },
            onMouseover: (e) => {
              e.target.style.color = COLOR_NORMAL;
              
            },
            onMouseout: (e) => {
              e.target.style.color = COLOR_HOVER;
            }
          },
          "ЛИЧНЫЙ КАБИНЕТ"
        ),
        key: "login",
      }
      
    ]
  }
    

})

const activeKey = ref(null);

onMounted(() => {
  checkScreen()
  window.addEventListener('resize', checkScreen)
  window.addEventListener('scroll', handleScroll)
  username.value = localStorage.getItem('username')
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <n-menu
    class="custom-menu desktop-menu"
    :class="{ 'menu-hidden': !isMenu }"
    v-model:value="activeKey"
    mode="horizontal"
    :options="menuOptions"
  />

  <button v-if="isMobile" class="burger-btn" :class="{ 'menu-hidden': !isMenu }" @click="isMobileMenuOpen = !isMobileMenuOpen" aria-label="Открыть меню">
    {{ isMobileMenuOpen ? '✕' : '☰' }}
  </button>

  <div v-if="isMobile && isMobileMenuOpen" class="mobile-dropdown" :class="{ 'menu-hidden': !isMenu }">
    <n-menu
      v-model:value="activeKey"
      mode="vertical"
      :options="menuOptions"
      @update:value="closeMobileMenu"
    />
  </div>

  <router-view />
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  overflow-x: hidden;
}

.custom-menu.n-menu {
  position: fixed !important;
  top: 0 !important;
  width: 100% !important;
  height: 10vh !important;  
  background-color: var(--bg-primary) !important;
  z-index: 1000 !important;
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out !important;
  border: 1px solid !important;
  padding: 0 !important;
  margin: 0 auto 0 auto !important;
}

.custom-menu.n-menu .n-menu__content {
  display: flex !important;
  justify-content: center !important;  
  align-items: center !important;          
  height: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 auto 0 auto !important ;
}

.custom-menu.n-menu .n-menu-item {
  flex: auto !important;  
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: 0 0 !important;
  padding: auto !important;
  font-size: var(--body);
  text-transform: uppercase;
}

.custom-menu.n-menu .n-menu-item-content {
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: calc((100% / 4) * 0,2)  !important;
}

.custom-menu.menu-hidden {
  transform: translateY(-100%);
  opacity: 0;
  pointer-events: none;
}

.burger-btn {
  position: fixed;
  top: 2vh; 
  right: 5vw;
  height: 10vh; 
  width: 40px;
  border: none;
  color: var(--accent); 
  font-size: var(--body);
  background: var(--bg-primary);
  z-index: 1002;
  display: none; 
  align-items: center; 
  justify-content: center;
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}
.burger-btn.menu-hidden {
  transform: translateY(-100%);
  opacity: 0; pointer-events: none;
}

.mobile-dropdown {
  position: fixed;
  top: 10vh; left: 0;
  width: 100%;
  background: rgba(10, 10, 10, 0.8);
  z-index: 1001;
  max-height: calc(100vh - 10vh);
  overflow-y: auto;
  border-bottom: 1px solid rgba(0, 177, 255, 0.3);
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.mobile-dropdown.menu-hidden {
  transform: translateY(-100%);
  opacity: 0; 
  pointer-events: none;
}

.mobile-dropdown .n-menu { 
  background: transparent !important; 
  border: none !important; 
}

.mobile-dropdown .n-menu-item-content {
  font-size: var(--body) !important; 
  text-transform: uppercase !important; 
  color: #fff !important;
  padding: 1.2rem 5vw !important; 
  border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  justify-content: flex-start !important; 
}

.custom-menu.menu-hidden {
  transform: translateY(-100%);
  opacity: 0; pointer-events: none;
}

@media (max-width: 768px) {
  .desktop-menu { display: none !important; }
  .burger-btn { display: flex !important; }
}

#app {
  padding-top: 10vh; 
  padding-left: 0;
  padding-right: 0;
  padding-bottom: 0;
}

</style>