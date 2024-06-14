<template>
    <div class="flex">
        <div class="me">
            <div class="flex align-items-center mt-3 flex-column">
                <div style="width: 72px; height: 72px; border-radius: 50%;" class="cursor-pointer"
                    @click="(e) => $refs.profile.toggle(e)">
                    <img v-if="user.image" :src="user.image" style="width: 100%;" />
                    <img v-else src="/images/user-big.svg" style="width: 100%;" />
                </div>
                <h2 class="text-center mt-3" style="font-size: 18px; color: var(--surface-900); font-weight: 600;">Иванов Сергей Викторович</h2>
                <p class="text-center" style="font-size: 14px;">khtkarimzhonov@gmail.com</p>
            </div>
            <div class="p-3">
                <NuxtLink :to="{name: 'me-locations'}">
                    <div class="profile-item" :class="{'profile-item-active': roote_name.startsWith('me-locations')}">
                        {{ $t('Участки') }}
                    </div>
                </NuxtLink>
                <NuxtLink :to="{name: 'me-cars'}">
                    <div class="profile-item" :class="{'profile-item-active': roote_name.startsWith('me-cars')}">
                        {{ $t('Авто') }}
                    </div>
                </NuxtLink>
                <NuxtLink :to="{name: 'me-users'}">
                    <div class="profile-item" :class="{'profile-item-active': roote_name.startsWith('me-users')}">
                        {{ $t('Участники') }}
                    </div>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>
<script>
import { useRoute } from 'vue-router';

export default {
    name: 'Profile',
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
.me {
    width: 240px;
    height: 100%;
    background-color: var(--surface-50);
    margin: 0;
}
.profile-item {
    padding: 18px 16px; 
    border-radius: 12px;
    font-weight: 500;
}

.profile-item-active {
    background-color: var(--primary-color-blur);
    color: var(--primary-color);
    font-weight: 600;
}
</style>