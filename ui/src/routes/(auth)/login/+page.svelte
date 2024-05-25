<script lang="ts">
  import { MailIcon, LockIcon } from 'lucide-svelte';
  import { user } from '$lib/stores';
  import { goto } from '$app/navigation';
  import { login } from '$lib/api-utils';

  let email = '';
  let password = '';

  async function submit() {
    const body = JSON.stringify({ email, password });
    const response = await login(body);
    if (!response.ok) {
      return;
    }
    $user = response.data;
    goto('/issues');
  }
</script>

<h1 class="text-xl font-medium leading-6">Увійти</h1>
<p class="text-sm text-navy-400">
  Немає облікового запису?
  <a href="/register" class="underline underline-offset-2">Зареєструватися</a>.
</p>
<hr class="mt-2 h-[1px] w-full border-0 bg-navy-800" />
<form on:submit|preventDefault={submit} class="mt-4 flex flex-col gap-4">
  <label class="inline-block">
    <span class="mb-2 block leading-4 text-navy-400">Електронна пошта</span>
    <div class="relative">
      <span
        class="pointer-events-none absolute left-2 top-1/2 flex -translate-y-1/2 items-center justify-center square-5"
      >
        <MailIcon class="text-navy-400 square-4" />
      </span>
      <input
        bind:value={email}
        type="text"
        placeholder="john@doe.com"
        class="h-10 w-full rounded-md border border-navy-200/10 bg-navy-900 pl-9 text-navy-50 transition-[border] placeholder:text-navy-500 focus-within:border-navy-100/20 focus-within:ring-2 focus-within:ring-navy-600 focus-within:ring-offset-2 focus-within:ring-offset-navy-900 hover:border-navy-100/20 focus:outline-none"
      />
    </div>
  </label>
  <label class="inline-block">
    <span class="mb-2 block leading-4 text-navy-400">Пароль</span>
    <div class="relative">
      <span
        class="pointer-events-none absolute left-2 top-1/2 flex -translate-y-1/2 items-center justify-center square-5"
      >
        <LockIcon class="text-navy-400 square-4" />
      </span>
      <input
        bind:value={password}
        type="text"
        placeholder="••••••••"
        class="h-10 w-full rounded-md border border-navy-200/10 bg-navy-900 pl-9 text-navy-50 transition-[border] placeholder:text-navy-500 focus-within:border-navy-100/20 focus-within:ring-2 focus-within:ring-navy-600 focus-within:ring-offset-2 focus-within:ring-offset-navy-900 hover:border-navy-100/20 focus:outline-none"
      />
    </div>
  </label>
  <button
    class="inline-flex h-11 w-full items-center justify-center rounded-md border border-navy-200/10 bg-navy-800 px-3 font-medium focus-within:ring-2 focus-within:ring-navy-600 focus-within:ring-offset-2 focus-within:ring-offset-navy-900 focus:outline-none"
  >
    Увійти
  </button>
</form>
