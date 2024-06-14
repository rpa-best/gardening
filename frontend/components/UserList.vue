<template>
    <div class="flex justify-content-between mt-5" style="width: 100%;">
        <div class="flex align-items-center">
            <h2 class="mb-0" style="color: var(--surface-900); font-size: 20px; font-weight: 600;">{{ $t('Учасники')
            }}</h2>
            <p class="ml-8 mb-0" style="font-size: 14px;">
                {{ $t('Кол-во') }}:
                <strong style="font-size: 18px; font-weight: 600; color: var(--surface-900);"
                    class="ml-2">1/2</strong>
            </p>
        </div>
    </div>
    <DataTable class="mt-3" :value="users.results" rowGroupMode="subheader" groupRowsBy="location.name" sortMode="single"
        sortField="location.name" :sort-order="1" @row-click="">
        <Column field="location.name" :header="$t('Локация')"></Column>
        <Column field="image" :header="$t('Фото')">
            <template #body="{ data }">
                <div style="width: 36px; height: 36px; border-radius: 8px;" class="cursor-pointer">
                    <Image v-if="data.image" preview :src="data.image" width="36" style="width: 100%;" />
                    <img v-else src="/images/user-big.svg" style="width: 100%;" />
                </div>
            </template>
        </Column>
        <Column field="first_name" :header="$t('Фамилия')">
            <template #body="{ data }">
                <span class="cursor-pointer" style="color: var(--secondory-color); font-size: 14px; font-weight: 600;" @click="(event) => {selected_user = data; $refs.cars.toggle(event)}">{{ data.first_name }}</span>
            </template>
        </Column>
        <Column field="last_name" :header="$t('Имя')"></Column>
        <Column field="surname" :header="$t('Отчество')"></Column>
        <Column field="email" :header="$t('Почта')"></Column>
        <Column field="event">
            <template #body="{ data }">
                <i class="pi pi-trash cursor-pointer" @click="confirm_delete($event, data)"></i>
            </template>
        </Column>
        <template #groupheader="slotProps">
        <div class="flex align-items-center gap-2 mt-3 mb-3">
            <strong style="color: var(--surface-900); font-size: 14px;">{{ slotProps.data.location.name }}</strong>
        </div>
    </template>
    </DataTable>
    <ConfirmPopup></ConfirmPopup>
    <OverlayPanel :ref="`cars`">
        <div class="user-cars">
            <Cars :params="{user: selected_user.id}" :readOnly="true" />            
        </div>
    </OverlayPanel>
</template>
<script>
import { useConfirm } from "primevue/useconfirm";
export default {
    name: "UserList",
    data() {
        return {
            users: {
                results: [
                    {
                        first_name: "Иванов",
                        last_name: "Андрей",
                        surname: "Владимирович",
                        email: "khtkarimzhonov@mail.ru",
                        location: {
                            name: "СНТ Девяткино, д. 24"
                        },
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
                    },
                    {
                        first_name: "Иванов",
                        last_name: "Андрей",
                        surname: "Владимирович",
                        email: "khtkarimzhonov@mail.ru",
                        location: {
                            name: "Пос. Парголово, уч 12"
                        },
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
                    },
                ]
            },
            selected_user: {},
            confirm: useConfirm(),
        }
    },
    methods: {
        confirm_delete(event, user) {
            this.confirm.require({
                target: event.currentTarget,
                message: this.$t(`Вы уверены, что хотите удалить учасника \"${user.first_name} ${user.last_name}\"?`),
                rejectClass: 'p-button-danger',
                acceptClass: 'p-button-primary-blur',
                rejectLabel: this.$t('Нет'),
                acceptLabel: this.$t('Да'),
                accept: () => {
                    this.$toast.add({ severity: 'success', summary: this.$t(`Пользователь удален успешно`), detail: `${user.first_name} ${user.last_name}`, life: 3000 });
                },
                reject: () => {}
            });
        }
    }
}
</script>
<style>
.user-cars .car-card {
    border: none !important
}
</style>