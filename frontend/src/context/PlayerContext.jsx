import { createContext, useContext, useState } from "react";
const PlayerContext = createContext(null);
export function PlayerProvider({ children }) {
  const [current, setCurrent] = useState(null);
  return <PlayerContext.Provider value={{ current, setCurrent }}>{children}</PlayerContext.Provider>;
}
export function usePlayer() { return useContext(PlayerContext); }
