<template>
    <div class="p-3" style="border: 2px solid var(--surface-border); border-radius: 12px;">
        <div class="flex justify-content-between" style="width: 100%;">
            <div class="flex align-items-center">
                <h2 class="mb-0" style="color: var(--surface-900); font-size: 20px; font-weight: 600;">{{ $t('Заявки')
                }}</h2>
                <p class="ml-8 mb-0" style="font-size: 14px;">
                    {{ $t('Кол-во') }}:
                    <strong style="font-size: 18px; font-weight: 600; color: var(--surface-900);" class="ml-2">2</strong>
                </p>
            </div>
        </div>
        <DataTable class="mt-3" :value="invites.results">
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
                    <span style="color: var(--surface-900); font-size: 14px;">{{ data.first_name }}</span>
                </template>
            </Column>
            <Column field="last_name" :header="$t('Имя')"></Column>
            <Column field="surname" :header="$t('Отчество')"></Column>
            <Column field="email" :header="$t('Почта')"></Column>
            <Column field="location.name" :header="$t('Адрес')"></Column>
            <Column field="event">
                <template #body="{ data }">
                    <i class="pi pi-check mr-3 cursor-pointer" style="color: var(--primary-color); font-weight: bold;" @click="accept($event, data)"></i>
                    <i class="pi pi-times ml-3 cursor-pointer" style="color: var(--danger-color); font-weight: bold;" @click="rejact($event, data)"></i>
                </template>
            </Column>
            <template #groupheader="slotProps">
                <div class="flex align-items-center gap-2 mt-3 mb-3">
                    <strong style="color: var(--surface-900); font-size: 14px;">{{ slotProps.data.location.name }}</strong>
                </div>
            </template>
        </DataTable>
        <ConfirmPopup></ConfirmPopup>
    </div>
</template>
<script>
import { useConfirm } from "primevue/useconfirm";

export default {
    name: "Invites",
    data() {
        return {
            invites: {
                results: [
                    {
                        first_name: "Иванов",
                        last_name: "Андрей",
                        surname: "Владимирович",
                        email: "khtkarimzhonov@mail.ru",
                        location: {
                            name: "СНТ Девяткино, д. 24"
                        },
                    },
                    {
                        first_name: "Иванов",
                        last_name: "Андрей",
                        surname: "Владимирович",
                        email: "khtkarimzhonov@mail.ru",
                        location: {
                            name: "СНТ Девяткино, д. 24"
                        },
                    },
                ]
            },
            selected_invite: {},
            confirm: useConfirm(),
        }
    },
    methods: {
        accept(event, user) {
            this.confirm.require({
                target: event.currentTarget,
                message: this.$t(`Вы уверены, что хотите принимать заявку \"${user.first_name} ${user.last_name}\"?`),
                rejectClass: 'p-button-danger',
                acceptClass: 'p-button-primary-blur',
                rejectLabel: this.$t('Отмена'),
                acceptLabel: this.$t('Да'),
                accept: () => {
                    this.$toast.add({ severity: 'success', summary: this.$t('Заявка принята'), detail: `${user.first_name} ${user.last_name}`, life: 3000 });
                },
                reject: () => {}
            });
        },
        rejact(event, user) {
            this.confirm.require({
                target: event.currentTarget,
                message: this.$t(`Вы уверены, что хотите откланить заявку \"${user.first_name} ${user.last_name}\"?`),
                rejectClass: 'p-button-danger',
                acceptClass: 'p-button-primary-blur',
                rejectLabel: this.$t('Отмена'),
                acceptLabel: this.$t('Да'),
                accept: () => {
                    this.$toast.add({ severity: 'success', summary: this.$t('Заявка отклонено'), detail: `${user.first_name} ${user.last_name}`, life: 3000 });
                },
                reject: () => {}
            });
        }
    }
}
</script>