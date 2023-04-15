<template>
  <v-app-bar
    color="teal-lighten-1"
    density="compact"
    dark
    class="mx-auto"
  >
    <v-toolbar-title>Energylevel Recalibration</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-menu>

      <v-btn icon="mdi-dots-vertical"></v-btn>

      <v-list>
        <v-list-item
          @click="() => {}"
        >
          <v-list-item-title>Revoke access & delete all my data</v-list-item-title>
        </v-list-item>
      </v-list>

    </v-menu>

  </v-app-bar>
</template>

<script setup>
//
</script>
