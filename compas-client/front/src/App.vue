<script setup>
import { NMenu, NIcon } from "naive-ui"; 
import { h, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";  
import { computed } from "vue";
const router = useRouter(); 

const username = ref('')
const isMenu = ref(true)
const lastScrollY = ref(0)

const isAutentificated = ref(!!localStorage.getItem('access_token'))

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
  window.addEventListener('scroll', handleScroll)
  username.value = localStorage.getItem('username')
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <n-menu
    class="custom-menu"
    :class="{ 'menu-hidden': !isMenu }"
    v-model:value="activeKey"
    mode="horizontal"
    :options="menuOptions"
  />
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
  left: 0 !important;
  width: 100% !important;
  height: 10vh !important;  
  background-color: #000000 !important;
  z-index: 1000 !important;
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out !important;
  border: 1px solid !important;
  padding: 0 !important;
  margin-left: calc((100% / 4) * 0,2);
}

.custom-menu.n-menu .n-menu__content {
  display: flex !important;
  justify-content: center !important;  
  align-items: center !important;          
  height: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin-left: 50px !important ;
}

.custom-menu.n-menu .n-menu-item {
  flex:  auto !important;  
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  margin: 0 0 !important;
  padding: auto !important;
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

#app {
  padding-top: 10vh; 
  padding-left: 0;
  padding-right: 0;
  padding-bottom: 0;
}

</style>