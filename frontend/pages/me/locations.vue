<template>
    <NuxtLayout name="me">
        <div style="padding: 24px 30px; width: 100%;">
            <h2 style="color: var(--surface-900); font-size: 20px;">{{ $t('Мои участки') }}</h2>
            <div class="row">
                <div class="col-3" style="padding: 8px;" v-for="location in locations">
                    <div class="location-card" @click="(e) => select_location(e, location)"
                    :class="{'location-card-active': (this.$route.query.location == location.id) && location.role == 'admin'} ">
                    <div class="flex justify-content-between align-items-center">
                        <strong>{{ location.name }}</strong>
                        <div v-if="location.role == 'admin'" @click="(e) => edit_location(e, location)"
                        style="padding: 8px 12px; border: 1px solid var(--surface-border); border-radius: 12px;" class="cursor-pointer">
                            <i class="pi pi-pencil" style="font-size: 12px;"></i>
                        </div>
                    </div>
                        
                        <p class="m-0">{{ location.city }}</p>
                        <p>{{ location.address }}</p>
                        <div v-if="location.role == 'user'">
                            <strong >{{ $t('Администратор') }}</strong>
                            <p class="m-0 mt-3">{{ location.admin.name }}</p>
                            <strong class="m-0" style="color: var(--primary-color)">{{ location.admin.phone }}</strong>
                        </div>
                        <div v-if="location.role == 'admin'">
                            <Button class="p-button-secondary" icon="pi pi-link" :label="$t('Скопировать приглашение')" @click="(e) => copy_link(e, location)" />
                        </div>
                    </div>
                </div>
            </div>
            <OverlayPanel :ref="`location`">
                <div class="p-3">
                    <div class="field"> 
                        <label for="name" class="block text-600 text-xl font-medium" style="font-size: 15px;">{{ $t('Адрес') }}<span class="ml-1" style="color: var(--primary-color)">*</span></label>
                        <InputText required id="name" type="text" :placeholder="$t('Введите адрес')" class="w-full" style="width: 100%;" v-model="editing_location.name" />
                    </div>
                    <div class="row mt-3">
                        <div class="col-6">
                            <Button class="p-button-close" :label="$t('Отмена')" @click="(e) => $refs[`location`].toggle(e)" />
                        </div>
                        <div class="col-6">
                            <Button :label="$t('Сохранить')" @click="save_location" />
                        </div>
                    </div>
                </div>
            </OverlayPanel>
            <div v-if="this.$route.query.location && selected_location.role == 'admin'">
                <div style="padding: 24px 0;">
                    <h2 style="color: var(--surface-900); font-size: 20px;">{{ $t('Камеры') }}</h2>
                    <div class="flex justify-content-between mb-3">
                        <div class="flex" style="border-radius: 12px; border: 1px solid var(--surface-border);">
                            <div class="cursor-pointer" :class="{active_group: active_group == i}" style="padding: 9px 16px; font-size: 12px;" v-for="group, i in selected_location.camera_groups" @click="active_group = i">
                                {{ group.name }}
                            </div>
                        </div>
                        <div>
                            <div style="padding: 9px 16px; font-size: 12px;border-radius: 12px; border: 1px solid var(--surface-border);">{{ $t('Настройки камер') }}</div>
                        </div>
                    </div>
                    <TabView class="cameras" v-model:activeIndex="active_group">
                        <TabPanel v-for="group in selected_location.camera_groups" :header="group.name">
                            <img src="/images/cameras-test.jpg" />
                            <div class="mt-3">
                                <Button class="p-button-secondary" style="font-size: 10px;" :label="$t('Открыть шлагбаум')" />
                            </div>
                        </TabPanel>
                    </TabView>
                </div>
                <div>
                    <h2 style="color: var(--surface-900); font-size: 20px;">{{ $t('События на локации') }}</h2>
                    <DataTable :value="history.results">
                        <Column field="date" :header="$t('Дата/Время')">
                            <template #body="{data}">
                                <span style="color: var(--secondory-color)">{{ data.date }}</span>
                            </template>
                        </Column>
                        <Column field="first_name" :header="$t('Фамилия')">
                            <template #body="{data}">
                                <span style="color: var(--surface-900)">{{ data.first_name }}</span>
                            </template>
                        </Column>
                        <Column field="last_name" :header="$t('Имя')"></Column>
                        <Column field="surname" :header="$t('Отчество')"></Column>
                        <Column field="car" :header="$t('Номер машины')"></Column>
                        <Column field="mode" :header="$t('Событие')">
                            <template #body="{data}">
                                {{ data.mode }} ({{ data.group_camera }})
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script>
export default {
    name: 'locations',
    data() {
        const location = {
            id: 1,
            name: "СНТ Девяткино, д. 24",
            city: "Санкт-Петербург",
            address: "СНТ Девяткино, д. 24",
            admin: {
                name: "Иванов Иван Иванович",
                phone: "+79215882553"
            },
            role: "admin",
            camera_groups: [
                {
                    id: 1,
                    name: 'Южный въезд',
                    cameras: [

                    ]
                },
                {
                    id: 1,
                    name: 'Северный въезд',
                    cameras: [

                    ]
                }
            ]
        }
        const locations = [
            location
        ]
        return {
            locations,
            selected_location: {},
            editing_location: {},
            active_group: 0,
            history: {}
        }
    },
    async mounted() {
        if (this.$route.query.location) {
            await this.fetch_location(this.$route.query.location)
        }
    },
    methods: {
        async fetch_location(location_id) {
            try {
                this.selected_location = this.locations[0]
                this.history = {
                    results: [
                        {
                            date: "06.04.24 19:34",
                            first_name: "Иванов",
                            last_name: "Андрей",
                            surname: "Владимирович",
                            car: "А55ВК78",
                            mode: "Въезд",
                            group_camera: "Северный въезд",
                        },
                        {
                            date: "06.04.24 19:34",
                            first_name: "Иванов",
                            last_name: "Андрей",
                            surname: "Владимирович",
                            car: "А55ВК78",
                            mode: "Въезд",
                            group_camera: "Южный въезд",
                        }
                    ]
                }
            } catch(e) {
                this.$router.push({name: this.$route.name})
            }
        },
        async select_location(e, location) {
            e.stopPropagation()
            const query = JSON.parse(JSON.stringify(this.$route.query))
            query.location = location.id
            this.$router.push({name: this.$route.name, query})
            await this.fetch_location(location.id)
        },
        edit_location(e, location) {
            e.stopPropagation()
            location = JSON.parse(JSON.stringify(location))
            this.editing_location = location
            this.$refs[`location`].toggle(e)
        },
        save_location(e) {
            this.$toast.add({ severity: 'success', summary: this.$t('Сохранено'), life: 1000 })
            this.$refs[`location`].toggle(e)
        },
        async copy_link(e, location) {
            e.stopPropagation()
            await navigator.clipboard.writeText("Link");
            this.$toast.add({ severity: 'success', summary: this.$t('Скапировано'), life: 1000 })
        }
    }
}
</script>

<style>
.location-card {
    border: 1px solid var(--surface-border);
    padding: 24px;
    border-radius: 12px;
    position: relative;
}
.location-card > * {
    color: var(--surface-900);
}

.location-card-active {
    border: 2px solid var(--primary-color);
}

.active_group {
    background-color: var(--surface-border);
    font-weight: 700;
    color: var(--surface-900);
}

.active_group:last-child {
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

.active_group:first-child {
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
}

.cameras .p-tabview-nav-container {
    display: none;
}
</style>