const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    console.log("Text copied to clipboard");
  });
};

const openInGoogle = (text) => {
  const url = `https://www.google.com/search?q=${encodeURIComponent(text)}`;
  window.open(url, "_blank");
};
const openInBing = (text) => {
  const url = `https://www.bing.com/search?q=${encodeURIComponent(text)}`;
  window.open(url, "_blank");
};
const openInDuckDuckGo = (text) => {
  const url = `https://duckduckgo.com/?q=${encodeURIComponent(text)}`;
  window.open(url, "_blank");
};

export { copyToClipboard, openInGoogle, openInBing, openInDuckDuckGo };
