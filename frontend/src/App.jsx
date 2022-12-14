import { createBrowserRouter, RouterProvider } from "react-router-dom";
// import HomePage, { loader as cardLoader } from "./TarotApp/pages/Home";
import Tarot, { loader as cardLoader} from "./TarotApp/pages/Tarot";
import NotesPage from "./TarotApp/pages/TarotSpreads";
import RootLayout from "./pages/RootLayout";
import Login from "./TarotApp/pages/Login";
import "./index.css";
import axios from "axios";
import Account from "./TarotApp/pages/Account";
import Dreams from "./DreamJournalApp/pages/Dreams";
import ForgotPassword from './pages/ForgotPassword'
import JournalEntries, { loader as journalLoader } from "./DreamJournalApp/pages/JournalEntries";
import HeroPage from "./pages/HeroPage";

export async function userLoader() {
  let res = await axios.get("api/user");
  let user = res.data;
  return { user };
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    loader: userLoader,
    children: [
      {
        index: true,
        element: <HeroPage user={userLoader} />,
        loader: cardLoader,
      },
      {
        path: "/tarot",
        // element: <NotesPage />,
        element: <Tarot />,
        loader: cardLoader
      },
      {
        path: "/dream",
        element: <Dreams />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/account",
        element: <Account />,
      },
      {
        path: "/journal",
        element: <JournalEntries />,
        loader: journalLoader,
      },
      {
        path: "/forgotpassword",
        element:<ForgotPassword/>
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
