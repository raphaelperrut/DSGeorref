import { mountProjectAccess } from "./index";
const container = document.getElementById("root");
if (!container) throw new Error("Project access root missing");
mountProjectAccess(container);
