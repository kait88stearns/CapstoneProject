def rse_bootstrap(X_train, y_train, num):
    RSEs = []
    for i in range(num):
        bootstrap = bootstrap_resample(np.c_[ X_train, y_train ])
        X_train = bootstrap[:, :-1]
        y_train = bootstrap[:, -1]
        gdbr.fit(X_train,y_train)
        y_hat=gdbr.predict(X_test)
        RSEs.append(np.sqrt(mean_squared_error(y_test, y_hat)))
    return np.array(RSEs)