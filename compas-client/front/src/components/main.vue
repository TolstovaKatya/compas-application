<template>
  <div class="logo">
    <span class="white-text">компас</span>
    <span class="blue-text">3D</span>
  </div>

  <div class="hero-section">
    <div class="hero-text">
      <div class="tagline">создание</div>
      <div class="tagline">трехмерных моделей</div>
      <div class="tagline">
        <span class="blue-text">легче,</span> чем ты думаешь
      </div>
    </div>

    <div class="hero-model">
      <Model 
        model-url="../../public/models/robobit_-_dex.glb"  
        :rotation-speed="0.04"
        :auto-rotate="true"
        class="model-component"
      />
    </div>

    <div class="hero-image-mobile">
    <img 
      src="../assets/images/photo_2025-09-27_23-51-10 1.png" 
      alt="3D модель Компас-3D"
      class="mobile-hero-img"
    />
  </div>
  </div>

  <div class="first-block" id="first-block">
    <div class="title">
      <span class="white-text">что такое</span>
      <span class="blue-text">компас 3d?</span>
    </div>
    <div class="first-block-content">
      <div class="line vertical"></div>
      <div class="line horizontal"></div>

      <div class="first-block-text">
        <span class="blue-text-first">КОМПАС-3D</span>
        <span class="white-text-first">
          - это полнофункциональная российская система автоматизированного проектирования, предназначенная для создания
          трехмерных моделей, комплексной разработки конструкторской документации и чертежей.<br><br>
          Это основное программное обеспечение для тысяч инженеров в машиностроении, приборостроении, авиа- и
          судостроении, а также идеальный инструмент для обучения и домашнего использования.
        </span>
      </div>

      <div class="first-block-img-wrapper">
        <img src="../assets/images/photo_2025-09-13_22-37-51 1.png" alt="второе изображение">
      </div>
    </div>
  </div>

  <div class="second-block" id="second-block">
    <div class="title">
      <span class="white-text">чему я</span>
      <span class="blue-text">научусь?</span>
    </div>
    <div class="second-block-content">
      <div class="second-block-text">
        <span class="white-text">
          Мечтаешь создавать 3D-модели как профессионал? На нашем сайте ты освоишь главный инструмент российских
          конструкторов -
        </span>
        <span class="blue-text">КОМПАС-3D</span><br><br>
        <span class="white-text">
          Наши пошаговые уроки и практические задания превратят тебя из новичка в уверенного пользователя. Забудь про
          скучные лекции — здесь только актуальные и нужные навыки для учебы и карьеры.
        </span><br><br>
        <span class="blue-text">Время творить!</span>
      </div>

      <n-carousel autoplay class="custom-carousel">
        <div class="carousel-slide column">
          <img class="carousel-img" :src="img" />
          <div class="carousel-caption-bottom">Модель робота</div>
        </div>
        <div class="carousel-slide column">
          <img class="carousel-img" :src="img1" />
          <div class="carousel-caption-bottom">Модель советского тяжёлого штурмового танка КВ-2</div>
        </div>
        <div class="carousel-slide column">
          <img class="carousel-img" :src="img3" />
          <div class="carousel-caption-bottom">Модель самолета АН-2</div>
        </div>
      </n-carousel>
    </div>
  </div>  

  <div class="third-block" id="third-block">
    <div class="title">
      <span class="white-text">из чего состоит</span>
      <span class="blue-text">курс?</span>
    </div>

    <div class="third-block-content">
      <span class="center-text">курс поделен на 2 основные части:</span>

      <div class="columns-wrapper">
        <div class="third-column third-left">
          <span class="main-text">основная</span>
          <span class="sub-text">
            Ты научишься создавать базовые чертежи, полностью освоишь программу и ее функционал.
            <br><br>
            Количество уроков: <span class="blue-text">XX</span>
          </span>
        </div>

        <div class="third-column third-right">
          <span class="main-text">усложненная</span>
          <span class="sub-text">
            Освоив базу, ты приступишь к созданию своей собственной трехмерной модели. Тебе будет предложено на выбор
            два варианта моделей.
            <br><br>
            Количество уроков: <span class="blue-text">XX</span>
          </span>
        </div>
      </div>
    </div>
  </div>


  <div class="fourth-block">
    <div class="title">
      <span class="white-text-fourth">ТРЕХМЕРНЫЕ<br>МОДЕЛИ,</span>
      <span class="white-text">КОТОРЫЕ</span>
      <span class="blue-text">ТЫ СМОЖЕШЬ</span>
      <span class="white-text">СДЕЛАТЬ</span>
    </div>

    <div class="fourth-block-content">
      <div class="card-item">
        <n-card hoverable class="model-card">
          <n-image :src="img" style="margin: 0 auto; display: block;" />
          <span class="card-title">МОДЕЛЬ МАШИНЫ</span>
          <n-button round color="#FFFFFF" text-color="#1D1D1B" class="view-btn">
            Посмотреть
          </n-button>
        </n-card>
      </div>

      <div class="card-item">
        <n-card hoverable class="model-card">
          <n-image :src="img1" style="margin: 0 auto; display: block;" />
          <span class="card-title">МОДЕЛЬ ТАНКА</span>
          <n-button round color="#FFFFFF" text-color="#1D1D1B" class="view-btn">
            Посмотреть
          </n-button>
        </n-card>
      </div>
    </div>
  </div> 
</template>

<script setup>
import { ref, computed } from 'vue';
import { NCard, NImage, NButton, NCarousel } from 'naive-ui';
import Model from '@/components/modelForMainPage.vue'; 

import img from '../assets/images/roobot.gif';
import img1 from '../assets/images/tank.png';
import img2 from '../assets/images/car.png';
import img3 from '../assets/images/airplane.png';
</script>

<style scoped>
:root {
  --accent: #00B1FF;
  --accent-hover: #009ce0;
  --text-main: #ffffff;
  --text-muted: #a0a0a0;
  --bg-primary: #000000;
  --bg-surface: #141414;
  --border: rgba(0, 177, 255, 0.3);
  --radius: 10px;
  
  --font-main: 'Arimo', system-ui, sans-serif;
  --h1: clamp(1.75rem, 5vw, 2.5rem); 
  --h2: clamp(1.5rem, 4vw, 2rem);    
  --h3: clamp(1.25rem, 3vw, 1.5rem); 
  --body: clamp(0.95rem, 2vw, 1.1rem); 
  --small: 0.875rem;
}

.logo {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 800;
  text-transform: uppercase;
  text-shadow: 0 0 20px rgba(0, 177, 255, 0.6);
  margin: 3vh auto 4vh;
  gap: 0.5rem;
  width: 100%;
  position: relative;
  z-index: 2;
}

.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 0;
  min-height: 60vh;
  gap: 1rem;
  position: relative;
}

.hero-text {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  z-index: 1;
  margin-left: 100px;
}

.tagline {
  font-size: var(--h1); 
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.2;
  color: var(--text-main);
  text-align: left;
}

.tagline .blue-text {
  color: var(--accent);
  text-shadow: 0 0 15px rgba(0, 177, 255, 0.5);
}

.hero-model {
  flex: 1.5;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 500px;
  position: relative;
  margin-top: -10vh;
  overflow: visible;
}

.model-component {
  width: 100%;
  max-width: 900px;
  height: 100%;
  pointer-events: none;
}

.white-text { color: var(--text-main) !important; }
.blue-text { color: var(--accent) !important; }
.white-text-fourth { color: var(--text-main); white-space: pre-wrap; font-size: var(--small); text-align: left; align-items: center;}

.white-text-first{ color: var(--text-main) !important; font-family: var(--body);}
.blue-text-first{ color: var(--accent) !important; font-family: var(--body);}


.title {
  font-size: var(--h1); 
  font-weight: 700;
  text-transform: uppercase;
  text-align: center;
  margin: 6vh 0 3vh;
  text-shadow: 0 0 15px rgba(0, 177, 255, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.first-block {
  padding: 4vh 5vw;
  max-width: 1200px;
  margin: 0 auto;
}

.first-block-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.first-block-text {
  font-size: var(--body);
  line-height: 1.6;
  color: var(--text-main);
}


.first-block-img-wrapper img {
  width: 80%;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 177, 255, 0.2);
}

.line { display: none; }

.second-block {
  padding: 4vh 5vw;
  max-width: 1200px;
  margin: 0 auto;
}

.second-block-text {
  font-size: var(--body) !important; 
  text-align: center;
  max-width: 900px;
  margin: 0 auto 3vh;
  color: var(--text-main);
}


.second-block-text .white-text,
.second-block-text .blue-text {
  font-size: inherit;
}

.custom-carousel {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
}

.carousel-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.carousel-caption-bottom {
  padding: 2rem;
  text-align: center;
  color: #aaa;
  font-size: var(--body); 
}

.third-block {
  padding: 4vh 5vw;
  max-width: 1200px;
  margin: 0 auto;
}

.third-block-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.center-text {
  font-size: var(--h3); 
  margin-bottom: 3rem;
  color: var(--text-main);
  font-weight: 600;
}

.columns-wrapper {
  display: flex;
  justify-content: center;
  gap: 4rem;
  width: 100%;
  flex-wrap: wrap;
}

.third-column {
  flex: 1;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(0, 177, 255, 0.2);
}

.main-text {
  color: var(--accent);
  font-size: var(--h3); 
  font-weight: 700;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.sub-text {
  color: var(--text-main);
  font-size: var(--body); 
  line-height: 1.5;
}

.fourth-block {
  padding: 4vh 5vw;
  max-width: 1200px;
  margin: 0 auto;
}

.fourth-block-content {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.card-item {
  flex: 1;
  min-width: 300px;
  max-width: 400px;
}

.model-card {
  background: #1a1a1a !important;
  color: white !important;
  border: 1px solid var(--accent) !important;
  border-radius: 12px !important;
  padding: 1.5rem !important;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s;
}

.model-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(0, 177, 255, 0.3);
}

.card-title {
  margin: 1rem 0;
  font-weight: bold;
  font-size: var(--body); 
}

.view-btn {
  width: 100%;
}

.hero-image-mobile {
  display: none; 
}

.mobile-hero-img {
  width: 100%;
  max-width: 400px;
  height: auto;
  box-shadow: 0 0 20px rgba(0, 177, 255, 0.3);
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;          
    min-height: auto;     
    justify-content: flex-start; 
    padding: 2vh 4vw;
  }

  .hero-text {
    align-items: center;
    width: 100%;
    margin-left: 0; 
    gap: 0.25rem;    
    text-align: center;     
  }

  .tagline {
    text-align: center;
  }

  .hero-image-mobile {
    display: flex;
    justify-content: center;
    margin-top: 0;       
    padding: 0;
  }

  .hero-model { 
    display: none; 
  }

  .first-block-content { 
    grid-template-columns: 1fr; 
  }

  .first-block-img-wrapper {
    order: -1;
    display: flex;
    justify-content: center;
    margin-bottom: 2rem; 
  }

  .first-block-img-wrapper img {
    width: 70%;         
    max-width: 100%;
  }

  .columns-wrapper { 
    flex-direction: column; 
    align-items: center; 
    gap: 2rem; 
  }

  .third-column { 
    width: 100%; 
  }

  .white-text-fourth {
    font-size: var(--h1);
    text-align: center;
    
    /* 👇 Заставляет элемент занять всю ширину строки */
    flex-basis: 100%; 
  }
}
</style>