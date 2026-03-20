<template>


    <div class="logo">
        <span class="white-text">компас</span>
        <span class="blue-text">3D</span>
    </div>

    <div class="img">
        <img src="../assets/images/photo_2025-09-27_23-51-10 1.png" alt="изображение на главной"/>
    </div>

    <div class="text-main" style="width: 1001px; height: 207px; position: relative">
        <div style="left: 394px; top: 0px; position: absolute; color: white; font-size: 48px; font-family: Arimo; font-weight: 400; text-transform: uppercase; word-wrap: break-word">создание</div>
        <div style="left: 0px; top: 76px; position: absolute; color: white; font-size: 48px; font-family: Arimo; font-weight: 400; text-transform: uppercase; word-wrap: break-word">трехмерных моделей</div>
        <div style="left: 374px; top: 152px; position: absolute"><span style="color: #00B1FF; font-size: 48px; font-family: Arimo; font-weight: 400; text-transform: uppercase; word-wrap: break-word">легче,</span><span style="color: white; font-size: 48px; font-family: Arimo; font-weight: 400; text-transform: uppercase; word-wrap: break-word"> чем ты думаешь</span></div>
    </div>

    <div class="first-block">
        <div class="title">
            <span class="white-text">что такое</span>
            <span class="blue-text">компас 3d?</span>
        </div>
        <div class="first-block-content">
            <div class="line" style="width: 1px; height: 456px; background-color: white; top: 28px; left: -23px"></div>
            <div class="line" style="width: 596px; height: 1px; background-color: white; top: 440px; left: -50px"></div>

            <div class="first-block-text">
                <span class="blue-text">КОМПАС-3D</span>
                <span class="white-text">
                    - это полнофункциональная российская система автоматизированного проектирования, предназначенная для создания трехмерных моделей, комплексной разработки конструкторской документации и чертежей.<br>
                    <br>
                    Это основное программное обеспечение для тысяч инженеров в машиностроении, приборостроении, авиа- и судостроении, а также идеальный инструмент для обучения и домашнего использования.
                </span>
            </div>
            <span>
                <img src="../assets/images/photo_2025-09-13_22-37-51 1.png" alt="второе изображениие">
            </span>
        </div>
    </div>

    <div class="second-block">
        <div class="title">
            <span class="white-text">чему я</span>
            <span class="blue-text">научусь?</span>
        </div>
        <div class="second-block-content">
            <div class="second-block-text">
                <span class="white-text">
                    Мечтаешь создавать 3D-модели как профессионал? На нашем сайте ты освоишь главный инструмент российских конструкторов - 
                </span>
                <span class="blue-text">КОМПАС-3D</span><br><br>
                <span class="white-text">
                    Наши пошаговые уроки и практические задания превратят тебя из новичка в уверенного пользователя. Забудь про скучные лекции — здесь только актуальные и нужные навыки для учебы и карьеры.
                </span><br><br>
                <span class="blue-text">Время творить!</span>
            </div>

            <div class="carousel-container">
                <div class="carousel">
                    <button class="carousel-btn-prev" @click="prevSlide" :disabled="currentIndex === 0">
                        <img src="../assets/images/prevButton.png" alt="">
                    </button> 
                    <div class="carousel-viewport">
                        <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * (100 / slidesToShow)}%)`}">
                            <div class="carousel-slide" v-for="(slide, index) in slides" :key="index">
                                <div class="carousel-card">
                                    <div class="line" style="width: 1px; height: 240px; background-color: white; left: 0; top: 50%; transform: translateY(-50%);"></div>
                                    <div class="line" style="width: 1px; height: 240px; background-color: white; right: 0; top: 50%; transform: translateY(-50%)"></div>
                                    <div class="line" style="width: 348px; height: 1px; background-color: white; top: 0; left: 50%; transform: translateX(-50%);"></div>
                                    <div class="line" style="width: 348px; height: 1px; background-color: white; bottom: 0; left: 50%; transform: translateX(-50%);"></div>
                                    <img :src="slide.image" :alt="slide.title">
                                    <span class="slide-title" style="color: white;">{{ slide.title }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="carousel-btn-next" @click="nextSlide" :disabled="currentIndex === maxIndex">
                        <img src="../assets/images/nextButton.png" alt="">
                    </button>
                </div>
            </div>
        </div>
    </div>  

    <div class="third-block">
        <div class="title">
            <span class="white-text">из чего состоит</span>
            <span class="blue-text">курс?</span>
        </div>
        <div class="third-block-content">
            <span class="center-text">курс поделен на 2 основные части:</span>
            <div class="third-left">
                <span class="main-left-text">
                    основная
                </span>
                <span class="left-text">
                    Ты научишься создавать базовые 
                    чертежи, полностью освоишь программу и 
                    ее функционал
                    <br><br>
                    Количесвто уроков:
                </span>
            </div>

            <div class="third-right">
                <span class="main-right-text">
                    усложненная
                </span>
                <span class="right-text">
                    Освоив базу, ты приступишь к
                    созданию своей собственной трехмерной
                    модели. Тебе будет предложено на 
                    выбор два варинта моделей.
                    <br><br>
                    Количество уроков:
                </span>
            </div>     
        </div>
    </div>

    <div class="fourth-block">
        <div class="title">
            <span class="white-text">
                ТРЕХМЕРНЫЕ
                МОДЕЛИ,
            </span>
            <span class="white-text">
                КОТОРЫЕ
            </span>
            <span class="blue-text">
                ТЫ СМОЖЕШЬ
            </span>
            <span class="white-text">
                СДЕЛАТЬ
            </span>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import img from '../assets/images/roobot.gif'
import img1 from '../assets/images/tank.png'
import img2 from '../assets/images/car.png'
import img3 from '../assets/images/airplane.png'
const slides = [
    { image: img1, title: 'Модель советского тяжёлого штурмового танка КВ-2'},
    { image: img2, title: 'Модель автомобиля ЗИС-5В'},
    { image: img3, title: 'Модель самолета АН-2'},
    { image: img, title: 'робот 4'},
    { image: img, title: 'робот 5'},
]

const slidesToShow = 3
const currentIndex = ref(0)
const maxIndex = computed(() => slides.length - slidesToShow)

const prevSlide = () => {
    if (currentIndex.value > 0) {
        currentIndex.value--
    }
}

const nextSlide = () => {
    if (currentIndex.value < maxIndex.value) {
        currentIndex.value++
    }
}
</script>

<style scoped>
.logo {
    display: flex;
    justify-content: center;
    font-family: 'Arimo';
    font-weight: bold;
    text-transform: uppercase;
    text-shadow: 4px 4px 40px rgba(0, 175, 255, 1);
    font-size: 100px;
    gap: 15px;
}

.white-text {
    color: white;
    white-space: pre-line;
}

.blue-text {
    color: #00B1FF;
}

@media (max-width: 768px) {
    .logo {
        font-size: 40px;
    }
}

.img {
    width: 654px; 
    height: 362px;
    margin: 21px 0px 0px 112px;
}

.text-main {
    margin: 31px 0px 0px 374px;
}

.title {
    display: flex;
    justify-content: center;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 48px;
    gap: 15px;
    text-shadow: 4px 4px 40px rgba(0, 175, 255, 1);
    margin-top: 233px;
}

.firs-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.first-block-text {
    max-width: 594px;
    text-align: left;
    margin-left: 174px;
    margin: 81px 133px 0px 0px;
    font-size: 24px;
}

.first-block-content {
    display: flex;
    position: relative;
    margin: 79px auto 0px auto;
    max-width: 1060px;
}

.line {
    position: absolute;
}

.second-block-text {
    max-width: 989px;
    font-size: 24px;
    text-align: center;
    margin: 56px auto 106px auto;
}

.carousel-container {
    width: 91%;
    margin: 0 auto 0 auto;
}

.carousel {
    position: relative;
    overflow: hidden;
}

.carousel-viewport {
    width: 87%;
    height: 100%;
    overflow: hidden;
    box-sizing: border-box;
    margin: 0 auto 0 auto;
}

.carousel-card {
    position: relative;
    width: 70%;
    height: 100%;
    margin: 0 2%;
}


.carousel-track {
    display: flex;
    transition: transform 0.4s ease;
}

.carousel-slide {
    min-width: calc(100% / 3);
    box-sizing: border-box;
    padding-top: 8px;
    padding-bottom: 8px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
}

.carousel-slide img {
    max-width: 305px;
    height: 167px;
    object-fit: cover;
    display: block;
    margin: auto;
}

.slide-title {
    display: block;
    font-size: 16px;
    padding-left: 35px;
    padding-bottom: 27px;
    max-width: 219px;
}

.carousel-btn-prev {
    background-color: black;
    width: 40px;
    height: 36px;
    border: none;
    position: absolute;
    display: flex;
    justify-items: center;
    align-items: center;
    transform: translateX(50%);
    top: 50%;
    z-index: 10;
    left: 0;
}

.carousel-btn-next {
    background-color: black;
    width: 40px;
    height: 36px;
    border: none;
    position: absolute;
    display: flex;
    justify-items: center;
    align-items: center;
    transform: translateX(-50%);
    top: 50%;
    z-index: 10;
    right: 0;
}

.third-block-content {
    position: relative;
    display: flex;
    justify-content: center;
}

.center-text {
    font-size: 24px;
    position: absolute;
    width: 100%;
    text-align: center;
    color: white;
    margin-top: 44px;
    text-transform: uppercase;
}

.third-left {
    position: absolute;
    width: 50vw;
    max-width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    left: 5%;
    top: 130px;
}

.third-right {
    position: absolute;
    width: 50vw;
    max-width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    right: 2%;
    top: 130px;
}

.main-left-text, .main-right-text {
    width: 100%;
    text-align: center;
    color: #00B1FF;
    text-transform: uppercase;
    white-space: pre-line;
    font-size: 32px;
    font-weight: bold;
}

.left-text, .right-text {
    width: 67%;
    color: white;
    text-align: center;
    white-space: pre-line;
    font-size: 24px;
    margin-top: 32px;
}
</style>