<script lang="ts">
  import { MenuIcon } from 'lucide-svelte';
  import {
    NewIssueDialog,
    Drawer,
    DrawerTrigger,
    DrawerContent,
    IssueList,
    SearchBar
  } from '$components';
  import { issues as initIssues } from '$lib';
  $: issues = $initIssues;

  function filter(e: CustomEvent<{ search: string }>) {
    issues = $initIssues.filter(
      c =>
        c.type.toLowerCase().includes(e.detail.search.toLowerCase()) ||
        c.description.toLowerCase().includes(e.detail.search.toLowerCase())
    );
  }

  let drawer: Drawer;
</script>

<Drawer bind:this={drawer}>
  <DrawerTrigger class="p-3">
    <MenuIcon class="square-4" />
  </DrawerTrigger>
  <DrawerContent class="flex flex-col p-0">
    <div
      class="flex h-20 w-full shrink-0 items-center border-b border-navy-200/10 px-2"
    >
      <SearchBar on:search={filter} />
    </div>
    <div class="w-full flex-1 overflow-y-auto p-2">
      <IssueList {issues} on:select={() => drawer.dismiss()} />
    </div>
    <div class="mt-auto h-20 max-h-20 w-full border-t border-t-navy-200/10">
      <div class="flex h-full items-center justify-center px-5">
        <NewIssueDialog />
      </div>
    </div>
  </DrawerContent>
</Drawer>
