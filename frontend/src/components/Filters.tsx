import { Filter } from 'lucide-react';

interface FiltersProps {
  selectedUser: string;
  selectedSource: string;
  users: string[];
  sources: string[];
  onUserChange: (user: string) => void;
  onSourceChange: (source: string) => void;
  onReset: () => void;
}

export function Filters({
  selectedUser,
  selectedSource,
  users,
  sources,
  onUserChange,
  onSourceChange,
  onReset,
}: FiltersProps) {
  const hasActiveFilters = selectedUser !== 'all' || selectedSource !== 'all';

  return (
    <div className="card mb-6">
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-gray-600" />
          <span className="text-sm font-medium text-gray-700">Filters:</span>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="source-filter" className="text-sm text-gray-600">
            Source:
          </label>
          <select
            id="source-filter"
            value={selectedSource}
            onChange={(e) => onSourceChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:border-transparent bg-white text-gray-900"
          >
            <option value="all">All Sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>
                {source === 'windsurf' ? 'Windsurf' : source === 'vscode_copilot' ? 'VS Code' : source}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="user-filter" className="text-sm text-gray-600">
            User:
          </label>
          <select
            id="user-filter"
            value={selectedUser}
            onChange={(e) => onUserChange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:border-transparent bg-white text-gray-900"
          >
            <option value="all">All Users</option>
            {users.map((user) => (
              <option key={user} value={user}>
                {user}
              </option>
            ))}
          </select>
        </div>

        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Reset Filters
          </button>
        )}

        {hasActiveFilters && (
          <div className="text-sm text-gray-600">
            {selectedSource !== 'all' && selectedUser !== 'all' && (
              <span>
                Showing {selectedSource === 'vscode_copilot' ? 'VS Code' : selectedSource} sessions for {selectedUser}
              </span>
            )}
            {selectedSource !== 'all' && selectedUser === 'all' && (
              <span>
                Showing {selectedSource === 'vscode_copilot' ? 'VS Code' : selectedSource} sessions
              </span>
            )}
            {selectedSource === 'all' && selectedUser !== 'all' && (
              <span>Showing sessions for {selectedUser}</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
