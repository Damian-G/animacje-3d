import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

//scena, kamera i renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

//kontrola myszką
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; 

//oświetlenie
scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const keyLight = new THREE.DirectionalLight(0xffeedd, 2.5);
keyLight.position.set(6, 8, 6);
scene.add(keyLight);

const fillLight = new THREE.DirectionalLight(0x9bcfff, 1.2);
fillLight.position.set(-6, 3, 4);
scene.add(fillLight);

const rimLight = new THREE.DirectionalLight(0x00ffcc, 3.5);
rimLight.position.set(0, 4, -6);
scene.add(rimLight);

//zmienne globalne
let mainModel = null;
let plantParts = [];
const clock = new THREE.Clock();

//ładowanie modelu
const infoElement = document.getElementById('info');
const loader = new GLTFLoader();

loader.load('biomech_13.glb', (gltf) => {
    mainModel = gltf.scene;
    scene.add(mainModel);
    
    //wszystkie części pąka do tablicy
    mainModel.traverse((child) => {
        if (child.isMesh) {
            if (child.name.toLowerCase().includes('sphere') || child.name.toLowerCase().includes('pąk')) {
                plantParts.push(child);
            }
        }
    });
    
    infoElement.innerText = `Model załadowany!`;
    
    //ustawienie kamery
    const box = new THREE.Box3().setFromObject(mainModel);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.6; 
    
    camera.position.set(center.x, center.y + size.y / 2, center.z + cameraZ);
    controls.target.copy(center);
    controls.update();
}, undefined, (error) => {
    infoElement.innerText = "Błąd ładowania modelu: " + error.message;
});

//skalowanie okna
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

//pętla animacji
function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    //obrót całego modelu
    if (mainModel) {
        mainModel.rotation.y = elapsedTime * 0.15;
    }

    //pulsowanie wszystkich części w tablicy
    if (plantParts.length > 0) {
        const scaleFactor = 1.0 + Math.sin(elapsedTime * 3.0) * 0.05;
        plantParts.forEach((part) => {
            part.scale.set(scaleFactor, scaleFactor, scaleFactor);
        });
    }

    controls.update(); 
    renderer.render(scene, camera);
}

animate();