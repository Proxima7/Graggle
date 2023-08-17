<template>
    <div class="grid grid-cols-2 gap-4">
        <div class="p-0 text-s">
            <font-awesome-icon :icon=icon />{{ title }}
        </div>
        <div class="p-0">
            <slot></slot>
        </div>
    </div>   
</template>

<script>
    export default {
        props: {
            icon: "fa-file",
            title: "myentry"
        }
    }
</script>