import { createContext, useEffect, useState } from 'react'
import { initializeApp } from 'firebase/app'
import {
  getAuth,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithCustomToken,
  signInAnonymously,
  onAuthStateChanged,
  signOut,
} from 'firebase/auth'

// create the auth context
export const AuthContext = createContext()

// this is the auth provider component
export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isAuthLoading, setIsAuthLoading] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [user, setUser] = useState(null)
  const [userData, setUserData] = useState(null);
  const [auth, setAuth] = useState(null)

  const firebaseConfig = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING,
    appId: import.meta.env.VITE_FIREBASE_APP_ID,
    measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
  }

  // effect will run once when the provider mounts to check the auth status
  useEffect(() => {
    // firebase initialization using the config
    setIsAuthLoading(true)
    const app = initializeApp(firebaseConfig)
    const authInstance = getAuth(app)
    setAuth(authInstance)

    const unsubscribe = onAuthStateChanged(authInstance, async (firebaseUser) => {
      setIsLoggedIn(!!firebaseUser);
      setUser(firebaseUser);
      setUserData(null);
      if(firebaseUser){
        // fetch user data from database
        // use stored token
        const token = localStorage.getItem("token");
        try{
          const response = await fetch('http://localhost:8000/users/user/email', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
          if(response.ok){
            const data = await response.json();
            setUserData(data);
          }
        }catch(e){
          console.error("Error fetching user data: ", e);
          setError(e);
        }
      }
      setIsAuthLoading(false)
    });

    return () => unsubscribe()
  }, [auth])

  const login = async (email, password) => {
    if (!auth) {
      setError('Authentication service not available')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const userCred = await signInWithEmailAndPassword(auth, email, password)
      const token = await userCred.user.getIdToken()

      localStorage.setItem('token', token)

      console.log('requesting user info')

      const response = await fetch('http://localhost:8000/users/user/email', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const user = await response.json()

      setUserData(user)
    } catch (err) {
      console.error('Firebase login failed: ', err.message)
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  // function to handle OAuth login with a popup
  const loginWithOAuth = async (provider) => {
    if (!auth) {
      setError('Authentication services are unavailable')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const userCred = await signInWithPopup(auth, provider)
      const token = await userCred.user.getIdToken()
      localStorage.setItem('token', token)
      const response = await fetch('http://localhost:8000/users/user/email', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const user = await response.json()
      setUserData(user)
    } catch (err) {
      console.error('Firebase OAuth login failed: ', err.message)
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const loginWithGoogle = () => loginWithOAuth(new GoogleAuthProvider())

  const logout = async () => {
    if (!auth) {
      setError('Authentication service is unavailable')
      return
    }

    setIsLoading(false)

    try {
      await signOut(auth)
      localStorage.removeItem('token')
    } catch (err) {
      console.error('Firebase logout failed: ', err.message)
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  // values provided to components wrapped by this provider
  const value = {
    isLoggedIn,
    isLoading,
    isAuthLoading,
    error,
    user,
    userData,
    login,
    logout,
    loginWithGoogle,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
