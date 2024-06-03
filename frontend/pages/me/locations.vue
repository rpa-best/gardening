<template>
    <NuxtLayout name="me">
        <div style="padding: 24px 30px;">
            <h2 style="color: var(--surface-900); font-size: 20px;">{{ $t('Мои участки') }}</h2>
            <div class="row">
                <div class="col-3" style="padding: 8px;" v-for="location in locations">
                    <div class="location-card" @click="() => select_location(location)"
                    :class="{'location-card-active': (this.$route.query.location == location.id) && location.role == 'admin'} ">
                        <strong>{{ location.name }}</strong>
                        <p class="m-0 mt-3">{{ location.city }}</p>
                        <p>{{ location.address }}</p>
                        <div v-if="location.role == 'user'">
                            <strong >{{ $t('Администратор') }}</strong>
                            <p class="m-0 mt-3">{{ location.admin.name }}</p>
                            <strong class="m-0" style="color: var(--primary-color)">{{ location.admin.phone }}</strong>
                        </div>
                        <div v-if="location.role == 'admin'">
                            <Button class="p-button-secondary" icon="pi pi-link" :label="$t('Скопировать приглашение')" />
                        </div>
                    </div>
                </div>
            </div>
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
                                <Button class="p-button-secondary" icon="pi pi-link" style="font-size: 10px;" :label="$t('Открыть шлагбаум')" />
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
        const locations = []
        for (let i = 0; i < 12; i ++) {
            locations.push(location)
        }
        return {
            locations,
            selected_location: location,
            active_group: 0,
            history: {
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
        }
    },
    methods: {
        select_location(location) {
            const query = JSON.parse(JSON.stringify(this.$route.query))
            query.location = location.id
            this.$router.push({name: this.$route.name, query})
        },
    }
}
</script>

<style>
.location-card {
    border: 1px solid var(--surface-border);
    padding: 24px;
    border-radius: 12px;
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