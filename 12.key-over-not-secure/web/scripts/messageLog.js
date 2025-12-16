export const createLogState = (users) =>
  users.reduce((acc, u) => {
    acc[u.name] = [];
    return acc;
  }, {});

export const pushLog = (logState, userName, entry) => {
  const list = logState[userName] || [];
  const hasCrypto = typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function';
  logState[userName] = [
    ...list,
    {
      ...entry,
      id: hasCrypto ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`
    }
  ];
};

export const getLog = (logState, userName) => logState[userName] || [];
