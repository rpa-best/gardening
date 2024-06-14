<template>
        <div v-if="!readOnly" class="flex justify-content-between" style="width: 100%;">
            <div class="flex align-items-center">
                <h2 class="mb-0" style="color: var(--surface-900); font-size: 20px; font-weight: 600;">{{ $t('Мои авто') }}</h2>
                <p class="ml-8 mb-0" style="font-size: 14px;">
                    {{ $t('Доступное кол-во') }}:
                    <strong style="font-size: 18px; font-weight: 600; color: var(--surface-900);" class="ml-2">1/2</strong>
                </p>
            </div>
            <Button class="p-button-secondary" style="font-size: 10px;" :label="$t('Добавить')" />
        </div>
        <div class="row">
            <div class="col-12 flex justify-content-between align-items-center car-card" v-for="car in cars" style="border: 1px solid var(--surface-border); padding: 16px; border-radius: 16px;">
                <div class="flex align-items-center">
                    <div style="border-radius: 12px; width: 96px; border-radius: 12px; overflow: hidden;">
                        <Image preview :src="car.image" width="96" style="width: 100%;" />
                    </div>
                    <div class="ml-8">
                        <strong style="color: var(--surface-900)">{{ car.model }}</strong>
                        <p class="mt-1 mb-0">{{ car.number }}</p>
                    </div>
                </div>
                <div>
                    {{ car.type }}
                </div>
                <div>
                    {{ car.create_date }}
                </div>
                <div v-if="!readOnly">
                    <i class="pi pi-ellipsis-h cursor-pointer"></i>
                </div>
            </div>
        </div>
</template>
<script>
export default {
    name: 'Cars',
    props: {
        params: {
            default: {}
        },
        readOnly: {
            default: false
        }
    },
    data() {
        return {
            cars: [
                {
                    id: 1,
                    image: "/images/car.jpg",
                    model: "Vesta",
                    number: "K228MH99",
                    type: "Легковой",
                    create_date: "06.04.2024"
                },
                {
                    id: 1,
                    image: "/images/car.jpg",
                    model: "Vesta",
                    number: "K228MH99",
                    type: "Легковой",
                    create_date: "06.04.2024"
                }
            ],
            user: {}
        }
    }
}
</script>
<style>
.car-card {
    margin-bottom: 1rem;
}

.car-card:last-child {
    margin-bottom: 0;
}
</style>