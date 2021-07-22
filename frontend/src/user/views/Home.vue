<template>
  <v-sheet
    class="toolbar-sheet"
    color="white"
    elevation="12"
    height="50"
    outlined
    rounded
    :width="styles.sheetWidth"
    :style="toolbarSheet"
  ></v-sheet>
</template>
<script>
export default {
  name: 'Home',
  data () {
    return {
      styles: {
        sheetWidth: 600
      }
    }
  },
  computed: {
    toolbarSheet () {
      return {
        top: '50px',
        left: '-webkit-calc(50% - ' + this.styles.sheetWidth/2 + 'px)' 
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .toolbar-sheet {
    position: relative;
  }
</style>
