<template>
    <div class="flex">
        <div class="sidebar">
            <div class="sidebar-button cursor-pointer flex justify-content-center align-items-center">
                <i class="pi pi-arrow-right" style="font-size: 10px;"></i>
            </div>
            <div>
                <NuxtLink :to="{name: 'index'}">
                    <img src="/images/logo.svg" />
                </NuxtLink>
            </div>
            <NuxtLink :to="{name: 'me'}">
                <div class="mt-3 p-2" :class="{selectded_sidebar: roote_name.startsWith('me')}">
                    <img src="/images/icons/profile.svg" width="25" />
                </div>
            </NuxtLink>
        </div>
        <div class="main">
            <div class="navbar flex justify-content-between align-items-center">
                <h1 class="m-0" style="font-size: 24px;">{{ $t('Главная') }}</h1>
                <div style="width: 32px; height: 32px; border-radius: 50%;" class="cursor-pointer" @click="(e) => $refs.profile.toggle(e)">
                    <img v-if="user.image" :src="user.image" style="width: 100%;" />
                    <img v-else src="/images/user-big.svg" style="width: 100%;" />
                </div>
                <OverlayPanel ref="profile">
                    <div class="p-3">
                        <div class=row>
                            <div class="col-3">
                                <div style="width: 48px; height: 48px; border-radius: 50%;" class="cursor-pointer" @click="(e) => $refs.profile.toggle(e)">
                                    <img v-if="user.image" :src="user.image" style="width: 100%;" />
                                    <img v-else src="/images/user-big.svg" style="width: 100%;" />
                                </div>
                            </div>
                            <div class="col-9">
                                <strong style="text-wrap: nowrap; color: var(--surface-900);">Иванов Сергей Викторович</strong>
                                <p class="mt-2" style="font-size: 12px;">khtkarimzhonov@gmail.com</p>
                            </div>
                        </div>
                        <div class="mt-3">
                                <strong>{{ $t('Тариф') }}</strong> 
                                <span class="cursor-pointer ml-6">{{ $t('Оптимальный') }}</span> 
                                <span class="cursor-pointer ml-6 pl-5 pr-5 pt-1 pb-1" style="background-color: #D8F9DA; border-radius: 8px; font-weight: bold; color: var(--primary-color)">{{ $t('Ултра') }}</span>
                            </div>
                            <div class="mt-4">
                                <strong class="cursor-pointer">{{ $t('Редактировать профиль') }}</strong> 
                            </div>
                            <div class="mt-4">
                                <strong class="cursor-pointer" style="color: var(--primary-color)">{{ $t('Выйти') }}</strong> 
                            </div>
                    </div>
                </OverlayPanel>
            </div>
            <slot />
        </div>
    </div>
</template>
  
<script>

import { useRoute } from 'vue-router';

export default {
    name: "main",
    data() {
        return {
            user: {}
        }
    },
    computed : {
        roote_name() {
            return useRoute().name
        }
    }
}
</script>
  
<style>
.main {
    width: 100%;
}
.sidebar {
    height: 100vh;
    width: 66px;
    border-right: 1px solid #EEEEEE;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
}

.sidebar-button {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 1px solid #EEEEEE;
    position: absolute;
    right: -12px;
    background-color: var(--surface-0);
    top: 20px;
}

.selectded_sidebar {
    background-color: var(--surface-50);
    border-radius: 12px;
    box-shadow: 0px 2px 0px 0px #D9D9D9;
}

.navbar {
    width: 100%;
    height: 64px;
    border-bottom: 1px solid #EEEEEE;
    padding: 0 30px;
}
</style>