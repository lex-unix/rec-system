<script lang="ts">
  import { issues as initIssues } from '$lib';
  import { SearchBar, IssueList, NewIssueDialog } from '$components';
  import { addToast } from '$components/Toaster.svelte';

  $: issues = $initIssues;

  function filter(e: CustomEvent<{ search: string }>) {
    issues = $initIssues.filter(
      c =>
        c.type.toLowerCase().includes(e.detail.search.toLowerCase()) ||
        c.description.toLowerCase().includes(e.detail.search.toLowerCase())
    );
  }

  function addIssue() {
    addToast({
      data: {
        title: 'Issue formed',
        description: 'New issue is registered'
      }
    });
  }
</script>

<div class="flex h-full max-h-full">
  <div
    class="relative hidden h-full w-full shrink-0 flex-col border-r border-navy-200/10 md:flex md:max-w-[340px] md:flex-col lg:max-w-[420px]"
  >
    <div
      class="flex h-20 w-full shrink-0 items-center border-b border-navy-200/10 md:px-3 lg:px-5"
    >
      <SearchBar on:search={filter} />
    </div>
    <div class="issues-list w-full flex-1 overflow-y-auto md:px-3 lg:px-5">
      <IssueList {issues} />
    </div>
    <div class="mt-auto h-20 max-h-20 w-full border-t border-t-navy-200/10">
      <div class="flex h-full items-center justify-center px-5">
        <NewIssueDialog on:add={addIssue} />
      </div>
    </div>
  </div>
  <slot />
</div>

<style lang="postcss">
  .issues-list {
    max-height: calc(100% - theme(spacing.20));
  }
</style>
