export const formatSourceName = (source: string): string => {
  if (source === 'vscode_copilot') {
    return 'VS Code';
  }
  if (source === 'windsurf') {
    return 'Windsurf';
  }
  return source.replace('_', ' ');
};
