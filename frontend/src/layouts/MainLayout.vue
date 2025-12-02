<template>
  <div class="main-layout">
    <el-container>
      <el-aside :width="sidebarWidth">
        <div class="logo">
          <h2>Alpha-Score</h2>
        </div>
        <el-menu
          :default-active="currentRoute"
          :collapse="appStore.sidebarCollapsed"
          router
        >
          <el-menu-item index="/dashboard">
            <el-icon><HomeFilled /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
          <el-menu-item index="/trading">
            <el-icon><TrendCharts /></el-icon>
            <template #title>交易监控</template>
          </el-menu-item>
          <el-menu-item index="/config">
            <el-icon><Setting /></el-icon>
            <template #title>配置管理</template>
          </el-menu-item>
          <el-menu-item index="/history">
            <el-icon><Clock /></el-icon>
            <template #title>历史数据</template>
          </el-menu-item>
          <el-menu-item index="/logs">
            <el-icon><Document /></el-icon>
            <template #title>日志查询</template>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header>
          <div class="header-left">
            <el-button
              :icon="appStore.sidebarCollapsed ? 'Expand' : 'Fold'"
              @click="appStore.toggleSidebar"
              text
            />
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="user-dropdown">
                <el-icon><User /></el-icon>
                {{ userStore.username || 'User' }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore, useAppStore } from '@/stores'
import { HomeFilled, User, ArrowDown, TrendCharts, Setting, Clock, Document } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

const currentRoute = computed(() => route.path)
const sidebarWidth = computed(() => (appStore.sidebarCollapsed ? '64px' : '200px'))

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.main-layout {
  width: 100%;
  height: 100vh;

  .el-container {
    height: 100%;
  }

  .el-aside {
    background-color: #304156;
    transition: width 0.3s;

    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 20px;
      border-bottom: 1px solid #1f2d3d;

      h2 {
        margin: 0;
        font-size: 18px;
      }
    }

    .el-menu {
      border-right: none;
      background-color: #304156;

      .el-menu-item {
        color: #bfcbd9;

        &:hover,
        &.is-active {
          background-color: #263445;
          color: #409eff;
        }
      }
    }
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    border-bottom: 1px solid #e4e7ed;
    padding: 0 20px;

    .header-left {
      display: flex;
      align-items: center;
    }

    .header-right {
      .user-dropdown {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        transition: background-color 0.3s;

        &:hover {
          background-color: #f5f7fa;
        }
      }
    }
  }

  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style>
