<script lang="ts">
  import { SearchBar, IssueList, NewIssueDialog } from '$components';
  import { addToast } from '$components/Toaster.svelte';
  import { onMount } from 'svelte';
  import type { Issue } from '$lib/types';
  import { createChat, createIssue } from '$lib/api-utils';

  let issues: Issue[] = [];

  onMount(async () => {
    const response = await fetch('http://localhost:8000/issues/', {
      credentials: 'include'
    });

    if (!response.ok) return;

    issues = await response.json();
  });

  async function addIssue(
    e: CustomEvent<{ subject: string; title: string; type: string }>
  ) {
    let body = JSON.stringify({ ...e.detail });
    const issueResponse = await createIssue(body);
    if (!issueResponse.ok) return;
    // console.log(issueResponse.data);

    body = JSON.stringify({ issueId: issueResponse.data.id });
    const chatResponse = await createChat(body);
    if (!chatResponse.ok) return;
    // console.log(chatResponse.data);

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
      <SearchBar />
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
