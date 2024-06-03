<template>
    <NuxtLayout name="main">
        <div class="flex" style="height: calc(100% - 64px)">
            <Profile />
            <slot />
        </div>
    </NuxtLayout>
</template>
