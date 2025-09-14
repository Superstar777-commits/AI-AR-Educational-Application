import React, { Suspense, useContext, useEffect, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { useSelector } from 'react-redux'

import { CSpinner, useColorModes } from '@coreui/react'
import './scss/style.scss'

// We use those styles to show code examples, you should remove them in your application.
import './scss/examples.scss'
import { AuthProvider, AuthContext } from './context/AuthContext'

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))

// Component that checks if the user is authenticated and redirects if not
const ProtectedRoute = ({children}) => {
  const {isLoggedIn, isAuthLoading} = useContext(AuthContext);

  if(isAuthLoading){
    return (
      <div className='pt-3 text-center'>
        <CSpinner color='primary' variant='grow' className='d-flex flex-col align-items-center justify-content-center' />
      </div>
    )
  }
  if(isLoggedIn == false){
    return <Navigate to="/login" replace/>
  }

  return children;
}

const App = () => {
  const { isColorModeSet, setColorMode } = useColorModes('coreui-free-react-admin-template-theme')
  const storedTheme = useSelector((state) => state.theme)
  const {isLoggedIn} = useContext(AuthContext);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.href.split('?')[1])
    const theme = urlParams.get('theme') && urlParams.get('theme').match(/^[A-Za-z0-9\s]+/)[0]
    if (theme) {
      setColorMode(theme)
    }

    if (isColorModeSet()) {
      return
    }

    setColorMode(storedTheme)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <BrowserRouter>
      <Suspense
        fallback={
          <div className="pt-3 text-center">
            <CSpinner color="primary" variant="grow" className='d-flex flex-col align-items-center justify-content-center' />
          </div>
        }
      >
        <Routes>
          <Route
            path="/"
            element={isLoggedIn === true ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
          />
          <Route exact path="/login" name="Login Page" element={<Login />} />
          <Route exact path="/register" name="Register Page" element={<Register />} />
          <Route exact path="/404" name="Page 404" element={<Page404 />} />
          <Route exact path="/500" name="Page 500" element={<Page500 />} />
          {/* Wrapping main routes in application with the ProtectedRoute component */}
          <Route
            path='*'
            name="Home"
            element={
              <ProtectedRoute>
                <DefaultLayout />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default () => (
  <AuthProvider>
    <App />
  </AuthProvider>
)
