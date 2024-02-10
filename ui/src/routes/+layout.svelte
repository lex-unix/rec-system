<script>
  import '../app.css';
</script>

<slot />

<style>
  :global(.no-scrollbar::-webkit-scrollbar) {
    display: none;
  }

  :gloabl(.no-scrollbar) {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
