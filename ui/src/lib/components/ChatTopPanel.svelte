<script lang="ts">
  import {
    InfoIcon,
    CheckCircle2Icon,
    MoreHorizontalIcon,
    Trash2Icon,
    CogIcon
  } from 'lucide-svelte';
  import {
    IssueInfo,
    Switch,
    SwitchButton,
    SwitchLabel,
    Popover,
    PopoverTrigger,
    PopoverContent,
    Dropdown,
    DropdownMenu,
    DropdownTrigger,
    DropdownItem,
    MobileIssuesDrawer
  } from '$components';
  import { issueType } from '$lib/issues';
  import { goto } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';
  import { addToast } from './Toaster.svelte';
  import { issues, issue, useChatbot } from '$lib/stores';
  import { deleteIssue } from '$lib/api-utils';
  import { page } from '$app/stores';

  const dispatch = createEventDispatcher();

  async function removeIssue() {
    const response = await deleteIssue($page.params.id);
    if (!response.ok) return;
    issues.remove(parseInt($page.params.id));
    goto('/issues');
    addToast({
      data: {
        title: 'Issue deleted',
        description: 'Issue successfully deleted from your list'
      }
    });
  }

  function resolve() {
    dispatch('resolve');
  }
</script>

<div
  class="relative flex h-20 items-center justify-between border-b border-navy-200/10 px-4"
>
  <div class="absolute inset-y-0 left-4 block md:hidden">
    <div class="flex h-full items-center">
      <MobileIssuesDrawer />
    </div>
  </div>
  {#if $issue}
    <h1 class="w-full text-center text-lg font-medium capitalize">
      {issueType[$issue.type]}
    </h1>
  {/if}

  <div class="absolute inset-y-0 right-4 pl-5">
    <div class="flex h-full items-center gap-5">
      <Popover>
        <PopoverTrigger class="rounded-full p-2">
          <CogIcon slot="icon" class="square-5" />
        </PopoverTrigger>
        <PopoverContent class="min-w-[360px]">
          <div>
            <h2 class="text-center text-lg font-medium">Налаштування чату</h2>
            <div class="pt-8">
              <Switch enabled={useChatbot}>
                <div class="flex items-center justify-between gap-3">
                  <SwitchLabel>Використовувати чат-бот?</SwitchLabel>
                  <SwitchButton />
                </div>
              </Switch>
            </div>
          </div>
        </PopoverContent>
      </Popover>
      <Popover>
        <PopoverTrigger class="rounded-full p-2">
          <InfoIcon slot="icon" class="square-5" />
        </PopoverTrigger>
        <PopoverContent>
          <IssueInfo />
        </PopoverContent>
      </Popover>
      <Dropdown>
        <DropdownTrigger class="rounded-full p-2">
          <MoreHorizontalIcon class="square-5" />
        </DropdownTrigger>
        <DropdownMenu>
          {#if $issue?.status !== 'closed'}
            <DropdownItem on:select={resolve}>
              <CheckCircle2Icon class="mr-3 square-5" />
              Закрити заявку
            </DropdownItem>
          {:else}
            <DropdownItem on:select={removeIssue}>
              <Trash2Icon class="mr-3 square-5" />
              Видалити заявку
            </DropdownItem>
          {/if}
        </DropdownMenu>
      </Dropdown>
    </div>
  </div>
</div>
