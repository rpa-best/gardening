<template>
    <NuxtLayout name="me">
        <div style="padding: 24px 30px; width: 100%;" >
            <div class="flex justify-content-between" style="width: 100%;">
                <h2 style="color: var(--surface-900); font-size: 20px;">{{ $t('События на локации') }}</h2>
                <Button class="p-button-secondary" style="font-size: 10px;" :label="$t('Добавить')" />
            </div>
            <div class="row">
                <div class="col-12 flex mt-3 justify-content-between align-items-center" v-for="car in cars" style="border: 1px solid var(--surface-border); padding: 16px; border-radius: 16px;">
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
                    <div>
                        <i class="pi pi-ellipsis-h cursor-pointer"></i>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>
<script>
export default {
    name: 'cars',
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
            ]
        }
    }
}
</script>
<style></style>