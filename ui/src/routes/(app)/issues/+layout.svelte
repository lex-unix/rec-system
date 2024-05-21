<script lang="ts">
  import { SearchBar, IssueList, NewIssueDialog } from '$components';
  import { addToast } from '$components/Toaster.svelte';
  import { onMount } from 'svelte';
  import {
    createChat,
    createIssue,
    fetchCustomerIssues,
    changeOperatoravAilability
  } from '$lib/api-utils';
  import { goto } from '$app/navigation';
  import { issues } from '$lib/stores';
  import { ISSUE_CREATED_TOAST_MSG } from '$lib/toast-messages';

  onMount(async () => {
    const respone = await fetchCustomerIssues();
    if (!respone.ok) return;
    $issues = respone.data;
  });

  async function addIssue(
    e: CustomEvent<{ subject: string; title: string; type: string }>
  ) {
    let body = JSON.stringify({ ...e.detail });
    const issueResponse = await createIssue(body);
    if (!issueResponse.ok) return;

    body = JSON.stringify({ issue_id: issueResponse.data.id });
    const chatResponse = await createChat(body);
    if (!chatResponse.ok) return;

    body = JSON.stringify({ availability: false });
    const operatorResponse = await changeOperatoravAilability(
      issueResponse.data.operator_id,
      body
    );

    if (!operatorResponse.ok) return;

    addToast(ISSUE_CREATED_TOAST_MSG);

    issues.add(issueResponse.data);

    goto(`/issues/${issueResponse.data.id}`);
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
      <IssueList />
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
