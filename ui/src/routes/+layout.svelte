<script>
  import '../app.css';
  import { Toaster } from '$components';
</script>

<slot />

<Toaster />

<style>
  :global(.no-scrollbar::-webkit-scrollbar) {
    display: none;
  }

  :gloabl(.no-scrollbar) {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
