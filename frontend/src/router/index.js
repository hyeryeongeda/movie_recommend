// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MoviesView from '@/views/MoviesView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/movies', name: 'movies', component: MoviesView },
  { path: '/movies/:id', name: 'movie-detail', component: MovieDetailView },
  { path: '/mypage', name: 'mypage', component: MyPageView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView }, 
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
