<template>
  <v-container fluid>
    <span>page #3</span>
    <p>
      {{ elasticSearch }}
    </p>
    <p>
      {{ detailSearch }}
    </p>
  </v-container>
</template>

<script>
export default {
  name: 'Page3',
  props: {
    elasticSearch: {
      type: String,
      default: null
    },
    detailSearch: {
      type: Object
    }
  }
}
</script>