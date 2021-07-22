<template>
  <v-toolbar
    dense
    floating
    class="toolbar-sheet"
    color="white"
    elevation="12"
    height="50"
    outlined
    rounded
    :width="styles.sheetWidth"
    :style="toolbarSheet"
  >
    <v-text-field
      hide-details
      append-icon="mdi-magnify"
      single-line
      :width="styles.sheetWidth"
    ></v-text-field>

    <v-btn icon>
      <v-icon>mdi-crosshairs-gps</v-icon>
    </v-btn>

    <v-btn icon>
      <v-icon>mdi-dots-vertical</v-icon>
    </v-btn>
  </v-toolbar>
  <!-- <v-sheet
    class="toolbar-sheet"
    color="white"
    elevation="12"
    height="50"
    outlined
    rounded
    :width="styles.sheetWidth"
    :style="toolbarSheet"
  ></v-sheet> -->
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      styles: {
        sheetWidth: 600,
        toolbarTop: 40
      }
    }
  },
  computed: {
    toolbarSheet () {
      return {
        top: this.styles.toolbarTop + 'vh'
        // left: '-webkit-calc(50% - ' + this.styles.sheetWidth/2 + 'px)' 
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .toolbar-sheet {
    position: relative;
  }
  .v-toolbar__content, .v-toolbar__extension {
    width: 600px;
  }
</style>
