<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import { Label, PinInputInput, PinInputRoot } from 'radix-vue'

defineEmits(['complete'])

const value = ref<string[]>([])

</script>

<template>
    <div class="flex flex-col" style="align-items: center;">
        <div class="text-center"><!--v-if--><p class="text-2xl text-gray-900 dark:text-white font-bold">Подтвердите телефон</p><!--v-if--></div>
        
            <PinInputRoot id="pin-input" v-model="value" placeholder="○" class="flex gap-2 items-center mt-1"
                @complete="(e) => $emit('complete', e)">
                <PinInputInput v-for="(id, index) in 4" :key="id" :index="index"
                    class="w-10 h-10 bg-white rounded text-center shadow-lg text-green10 placeholder:text-mauve8 focus:outline focus:outline-2 focus:outline-offset-2 focus:outline-white" />
            </PinInputRoot>
        

    </div>
</template>