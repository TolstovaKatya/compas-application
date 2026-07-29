<template>
  <div ref="container" class="hero-3d"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const props = defineProps({
  modelUrl: { type: String, required: true },
  rotationSpeed: { type: Number, default: 0.003 },
  autoRotate: { type: Boolean, default: true }
});

const container = ref(null);
let scene, camera, renderer, model, animationId;
let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;

const init = () => {
  if (!container.value) return;

  // сцена
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0a); 

  // камера
  camera = new THREE.PerspectiveCamera(
    45,
    container.value.clientWidth / container.value.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 5;

  // рендерер
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.value.clientWidth, container.value.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  container.value.appendChild(renderer.domElement);

  // освещение 
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);
  
  const mainLight = new THREE.DirectionalLight(0x00B1FF, 0.8); 
  mainLight.position.set(5, 5, 5);
  scene.add(mainLight);
  
  const fillLight = new THREE.DirectionalLight(0xffffff, 0.4);
  fillLight.position.set(-5, -5, -5);
  scene.add(fillLight);

  // загрузка модели
  const loader = new GLTFLoader();
  loader.load(
    props.modelUrl,
    (gltf) => {
      model = gltf.scene;
      model.scale.set(2.25, 2.25, 2.25); 
      model.position.y = -0.2;
      scene.add(model);
    },
    undefined,
    (err) => console.error('Ошибка загрузки модели:', err)
  );

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('touchmove', onTouchMove, { passive: true });
  window.addEventListener('resize', onResize);

  const animate = () => {
    animationId = requestAnimationFrame(animate);
    
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;
    
    if (model) {
      model.rotation.y += targetX * props.rotationSpeed;
      model.rotation.x -= targetY * props.rotationSpeed * 0.5;
      
      if (props.autoRotate && Math.abs(mouseX) < 0.01 && Math.abs(mouseY) < 0.01) {
        model.rotation.y += 0.002;
      }
    }
    
    renderer.render(scene, camera);
  };
  animate();
};

const onMouseMove = (e) => {
  mouseX = (e.clientX / window.innerWidth) * 2 - 1;
  mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
};

const onTouchMove = (e) => {
  if (e.touches[0]) {
    mouseX = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
    mouseY = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
  }
};

const onResize = () => {
  if (!container.value) return;
  camera.aspect = container.value.clientWidth / container.value.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.value.clientWidth, container.value.clientHeight);
};

const cleanup = () => {
  cancelAnimationFrame(animationId);
  document.removeEventListener('mousemove', onMouseMove);
  document.removeEventListener('touchmove', onTouchMove);
  window.removeEventListener('resize', onResize);
  if (renderer) {
    renderer.dispose();
    renderer.domElement?.parentNode?.removeChild(renderer.domElement);
  }
  if (model) {
    model.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) {
          obj.material.forEach(m => m.dispose());
        } else {
          obj.material.dispose();
        }
      }
    });
  }
  scene = null;
};

onMounted(() => {
  setTimeout(init, 100);
});

onBeforeUnmount(() => {
  cleanup();
});
</script>

<style scoped>
.hero-3d {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; 
  z-index: 0;
}

@media (max-width: 768px) {
  .hero-3d {
    display: none;
  }
}
</style>