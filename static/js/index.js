import './utils.js';
import '../css/main.css';
import * as THREE from '../../node_modules/three/build/three.module.js';
import { MapControls } from '../../node_modules/three/examples/jsm/controls/OrbitControls.js' ;
import { GUI } from '../../node_modules/three/examples/jsm/libs/dat.gui.module.js';
import { Line2 } from '../../node_modules/three/examples/jsm/lines/Line2.js';
import { LineMaterial } from '../../node_modules/three/examples/jsm/lines/LineMaterial.js';
import { BufferGeometryUtils } from '../../node_modules/three/examples/jsm/utils/BufferGeometryUtils.js';
import { GLTFLoader } from '../../node_modules/three/examples/jsm/loaders/GLTFLoader.js';