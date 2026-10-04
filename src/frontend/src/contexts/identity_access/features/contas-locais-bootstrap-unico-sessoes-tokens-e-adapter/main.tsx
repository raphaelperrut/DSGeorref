import { mountIdentitySurface } from "./index";

const root = document.getElementById("root");
if (!root) throw new Error("Identity surface root is missing");
mountIdentitySurface(root);
