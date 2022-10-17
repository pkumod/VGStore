<template>
    <vue-json-pretty
        :data="data"
        :showLine="true"
        :showDoubleQuotes="true"
        :highlightMouseoverNode="true"
        :collapsedOnClickBrackets="true"
        :deep="2"
    >
    </vue-json-pretty>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
    name: 'JSONResult',
    components: {VueJsonPretty},
    props: ['data']
}
</script>
